import mss
import numpy as np
from PIL import Image
import cv2
import time
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

from logitech_driver import Logitech
from random_delay import random_delay_ms
# 添加兼容性补丁
if not hasattr(np, 'asscalar'):
    np.asscalar = lambda x: x.item()

def custom_screenshot(bounding_box=None):
    """
    截图并识别文字。

    参数:
        bounding_box: 截图区域的边界框，格式为 (left, top, right, bottom)。

    返回:
        识别出的文字。
    """
    # 使用 mss 截图
    with mss.mss() as sct:
        # 获取屏幕上的第一个显示器信息
        if bounding_box:
            monitor = bounding_box
        else:
            monitor = sct.monitors[0]

        # 捕获屏幕截图
        screenshot = sct.grab(monitor)

        # 将截图转换为 numpy 数组并转换为 RGB 格式
        image = np.array(screenshot)[:, :, :3]  # 去掉透明通道（A），只保留 RGB
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
       
    return image
# 保存图像为文件
def save_image(image, output_path):
    """
    保存 NumPy 数组格式的图像到文件。

    参数:
        image: NumPy 数组格式的图像。
        output_path: 图像保存的路径。
    """
    # 创建图片对象
    screenshot_image = Image.fromarray(image, mode='RGB')
    
    # 保存图片p
    screenshot_image.save(output_path)



def hsv_value(rgb):
    return cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)[0][0]

def is_red(hsv, min_s=50, min_v=50):
    h, s, v = hsv
    # 检查色相是否在红色区间
    red_low = (h >= 0) and (h <= 15)
    red_high = (h >= 165) and (h <= 180)
    # 检查饱和度和明度是否足够
    return (red_low or red_high) and (s >= min_s) and (v >= min_v)

def check_pixel_surrounding(image_input, target_rgb1, target_rgb2, similarity_threshold=1, from_bgr=True):
    """
    检查图片中是否存在符合规则的像素点.

    参数:
        image_input: 图片的路径或者 NumPy 数组格式的图像 (BGR 格式).
        target_rgb1: 第一种目标 RGB 颜色值，如 (0, 0, 0) 代表黑色.
        target_rgb2: 第二种目标 RGB 颜色值，如 (242, 74, 23).
        similarity_threshold: 颜色相似度阈值（0 到 1，0 表示最不相似，1 表示完全相同）.
        from_bgr: 是否将输入的图像从 BGR 转换为 RGB (默认为 True).
        
    返回:
        是否存在符合规则的像素点.
    """
    # 判断输入是图片路径还是图像对象
    if isinstance(image_input, str):
        # 从路径加载图像
        img = cv2.imread(image_input)
    else:
        # 图像是 NumPy 数组格式
        img = image_input.copy()

    # 转换为 RGB 格式 (如果需要)
    if from_bgr:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        rgb_img = img.copy()

    # 保存截图
    # output_path = "screenshot.png"
    # save_image(rgb_img, output_path)
    # print(f"截图已保存为 {output_path}")    
    # 获取图像的高度和宽度
    height, width, _ = rgb_img.shape

    # 遍历图像中的每个像素
    for y in range(height):
        for x in range(width):
            current_pixel = rgb_img[y, x]
            #判断当前点是否在红色范围内
            if ( not is_red(hsv_value(current_pixel)) ): continue  
            # 检查当前像素相似度是否满足
            if (color_similarity_rgb(target_rgb2,current_pixel) >= similarity_threshold):
                # 收集上下左右四个相邻像素
                neighbors = []
                # 上
                if y > 0:
                    neighbors.append(rgb_img[y-1, x])
                # 下
                if y < height - 1:
                    neighbors.append(rgb_img[y+1, x])
                # 左
                if x > 0:
                    neighbors.append(rgb_img[y, x-1])
                # 右
                if x < width - 1:
                    neighbors.append(rgb_img[y, x+1])
                # print(neighbors,target_rgb1,target_rgb2)
                # 检查邻居像素是否至少包含一个 target_rgb1 和至少一个 target_rgb2
                has_target1 = any((neighbor == target_rgb1).all() for neighbor in neighbors)
                has_target2 = any((neighbor == current_pixel).all() for neighbor in neighbors)
                if has_target1 and has_target2:
                    #print(color_similarity_rgb(target_rgb2,current_pixel),current_pixel,target_rgb2)
                    # # 保存截图
                    # output_path = "out.png"
                    # save_image(rgb_img, output_path)
                    # print(f"截图已保存为 {output_path}") 
                    # print(f"符合条件的像素p点位于 (x={x}, y={y})")
                    return True  # 找到一个符合条件的像素点，返回 True

    # 遍历完整张图片未找到符合条件的像素点，返回 False
    # print("未找到符合条件的像素点")
    return False


#基于 RGB欧氏距离 
def color_similarity_rgb(rgb1, rgb2):
    """计算 RGB 颜色相似度（0-1，1为完全相等）"""
    # 计算欧氏距离
    distance = sum((c1 - c2)**2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5
    # print(distance)
    # 最大可能距离（黑到白）：√(255² + 255² + 255²) ≈ 441.67
    max_distance = (255**2 * 3) ** 0.5
    # 归一化到 0-1 并反转（1表示完全相似）
    similarity = 1 - (distance / max_distance)
    # print(round(similarity, 2))
    return round(similarity, 2)

#基于 CIELAB Delta E 2000
def color_similarity(rgb1, rgb2):
    # 转换RGB到sRGBColor对象
    color1 = sRGBColor(rgb1[0], rgb1[1], rgb1[2], is_upscaled=True)
    color2 = sRGBColor(rgb2[0], rgb2[1], rgb2[2], is_upscaled=True)
    # 转换为Lab颜色空间
    lab1 = convert_color(color1, LabColor)
    lab2 = convert_color(color2, LabColor)
    # 计算Delta E 2000
    delta_e = delta_e_cie2000(lab1, lab2)
    # 将Delta E转换为0-1的相似度，最大值设为100
    similarity = max(0.0, 1.0 - delta_e / 100.0)
    return round(similarity, 2)  # 保留2位小数
def fast_rgb_similarity(rgb1, rgb2):
    """基于加权欧氏距离的近似算法"""
    r_mean = (rgb1[0] + rgb2[0]) / 2
    r = rgb1[0] - rgb2[0]
    g = rgb1[1] - rgb2[1]
    b = rgb1[2] - rgb2[2]
    return 1 - np.sqrt((2 + r_mean/256)*r**2 + 4*g**2 + (2 + (255 - r_mean)/256)*b**2) / 1400

def autoFire(globals_instance):
    bounding_box = (800-14, 500, 800+14, 514) #1600x900
    rgb_a = (0, 0, 0)
    rgb_b = (242, 74, 23)
    rgb_c = (177, 60, 45)
    rgb_d = (160, 57, 50)
    rgb_e = (154, 55, 52)
    rgb_Center = (198, 65, 38)

    image = custom_screenshot(bounding_box)
    isFire = check_pixel_surrounding(image, rgb_a, rgb_Center, globals_instance.similarity)
    if (isFire):
        random_delay_ms(globals_instance.fireDelay,globals_instance.fireDelay+10)
        if(globals_instance.jujiqiang):
            print('jujiqiang')
            Logitech.mouse.click(2)
            random_delay_ms(40,60)
            Logitech.keyboard.click(globals_instance.firebtn)
            random_delay_ms(50,80)


        elif(globals_instance.buqiang):
            Logitech.keyboard.click(globals_instance.firebtn)
            random_delay_ms(3,15)
            Logitech.mouse.move(x=0,y=2)
            

                
        else:
            1
        # Logitech.keyboard.press(globals_instance.firebtn)
        # random_delay_ms(10,20)
        # Logitech.keyboard.release(globals_instance.firebtn)
        # print('开火')


def worker_auto_fire(globals_instance):
    while True:
        if(globals_instance.auto_fire):
            autoFire(globals_instance)
        else:
            time.sleep(1)
        


# while True:
#     start=time.time()
#     color_similarity(color1,color2)


#     end=time.time()
#     print(end-start)
# Logitech.mouse.move(x=0,y=2)
