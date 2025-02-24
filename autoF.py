import mss
import numpy as np
from PIL import Image
import cv2
import time
from logitech_driver import Logitech


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
        # # 保存截图
        # output_path = "screenshot.png"
        # save_image(image, output_path)
        # print(f"截图已保存为 {output_path}")
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



def v_value(rgb):
    return cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_BGR2HSV)[0][0][2]
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

    # 获取图像的高度和宽度
    height, width, _ = rgb_img.shape

    # 遍历图像中的每个像素
    for y in range(height):
        for x in range(width):
            current_pixel = rgb_img[y, x]
            # 检查当前像素是否是 target_rgb2
            if (current_pixel == target_rgb2).all():
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

                # 检查邻居像素是否至少包含一个 target_rgb1 和至少一个 target_rgb2
                has_target1 = any((neighbor == target_rgb1).all() for neighbor in neighbors)
                has_target2 = any((v_value(neighbor) / v_value(target_rgb2) >= similarity_threshold).all() for neighbor in neighbors)
                if has_target1 and has_target2:
                    print(f"符合条件的像素点位于 (x={x}, y={y})")
                    return True  # 找到一个符合条件的像素点，返回 True

    # 遍历完整张图片未找到符合条件的像素点，返回 False
    # print("未找到符合条件的像素点")
    return False

def autoFire(globals_instance):
    bounding_box = (800-14, 500, 800+14, 514)
    image = custom_screenshot(bounding_box)
    isFire = check_pixel_surrounding(image,(0, 0, 0), (242, 74, 23),0.8)
    if (isFire):
        Logitech.keyboard.click(globals_instance.firebtn)
        print('开火')


def worker_auto_fire(globals_instance):
    while True:
        if(globals_instance.auto_fire):
            autoFire(globals_instance)
        else:
            time.sleep(0.002)


# if __name__ == "__main__":
#     # 设置截图区域和间隔
#     # bounding_box = (1650, 940, 1900, 1000)
#     bounding_box = (800-14, 500, 800+14, 514)
#     # while True:
#     # custom_screenshot(bounding_box)
#     check_pixel_surrounding('1.png',(0, 0, 0), (242, 74, 23),0.8)
#       # time.sleep(0.01)
        

    