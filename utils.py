import pyautogui
import win32gui
import mss
import numpy as np
from PIL import Image
import cv2
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from collections import Counter

game_dict = {
    1: {
        "red_name_box": (800 - 14, 500, 800 + 14, 500 + 14),
        "weapon_Identify_box": (1414, 812 - 2, 1588, 812 + 14 + 2),
    },
    2: {
        "red_name_box": (960 - 18, 600, 960 + 18, 600 + 18),
        "weapon_Identify_box": (1690, 974 - 2, 1905, 974 + 18 + 2),
    },
    3: {
        "red_name_box": (1280 - 20, 802, 1280 + 20, 802 + 20),
        "weapon_Identify_box": (2270, 1301 - 2, 2542, 1301 + 20 + 2),
    },
    "jtl": "加林炼狱",
    "usp": "uspUSPcopCOP沙鹰",
    "ju": "BarrettAWM98K",
}


def custom_screenshot(bounding_box=None):
    """
    全屏范围截图。

    参数:
        bounding_box: 截图区域的边界框，格式为 (left, top, right, bottom)。

    返回:
        图片rgb格式 numpy 数组。
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

        # 将截图转换为 numpy 数组
        image = np.array(screenshot)[:, :, :3]  # 去掉透明通道（A），只保留 RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


# 保存图像为文件
def save_image(image, output_path="out.png"):
    """
    保存 NumPy 数组格式的图像到文件。

    参数:
        image: NumPy 数组格式的图像。
        output_path: 图像保存的路径。
    """
    # 创建图片对象
    screenshot_image = Image.fromarray(image, mode="RGB")

    # 保存图片p
    screenshot_image.save(output_path)


def find_image_in_screenshot(screenshot, target_image_path, threshold=0.8):
    """
    在截图中查找目标图片，并返回目标图片的中心坐标。

    参数:
        screenshot: 截图的 RGB 格式 numpy 数组。
        target_image_path: 目标图片的路径。
        threshold: 匹配阈值0-1
    返回:
        如果找到目标图片，返回目标图片的中心坐标 (x, y)；
        如果未找到，返回 None。
    """
    # 读取目标图片
    target_image = cv2.imread(target_image_path)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)

    # 转换为灰度图像
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
    target_image_gray = cv2.cvtColor(target_image, cv2.COLOR_RGB2GRAY)

    # 进行模板匹配
    result = cv2.matchTemplate(screenshot_gray, target_image_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # 获取目标图片的宽度和高度
        target_height, target_width = target_image_gray.shape
        # 计算中心坐标
        center_x = max_loc[0] + target_width // 2
        center_y = max_loc[1] + target_height // 2
        return center_x, center_y
    else:
        return None


def hsv_value(rgb):
    return cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)[0][0]


# 基于 RGB欧氏距离
def color_similarity_rgb(rgb1, rgb2):
    """计算 RGB 颜色相似度（0-1，1为完全相等）"""
    # 将颜色值转换为浮点数
    rgb1 = [float(c) for c in rgb1]
    rgb2 = [float(c) for c in rgb2]
    # 计算欧氏距离
    distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)) ** 0.5
    # print(distance)
    # 最大可能距离（黑到白）：√(255² + 255² + 255²) ≈ 441.67
    max_distance = (255**2 * 3) ** 0.5
    # 归一化到 0-1 并反转（1表示完全相似）
    similarity = 1 - (distance / max_distance)
    # print(round(similarity, 2))
    return round(similarity, 2)


# 基于 CIELAB Delta E 2000
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
    return (
        1
        - np.sqrt(
            (2 + r_mean / 256) * r**2 + 4 * g**2 + (2 + (255 - r_mean) / 256) * b**2
        )
        / 1400
    )


def click_for_img(img, x=0, y=0):
    """x,y偏移量"""
    xy = find_image(img)
    # print(xy)
    if not xy:
        return
    click((xy[0] + x, xy[1] + y))


def click(len):
    click_x = int(len[0])
    click_y = int(len[1])
    # 移动鼠标并点击


def find_image(template_path, box=None, threshold=0.8):
    # 截图
    screenshot = custom_screenshot(box)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # 加载目标图像
    template = cv2.imread(template_path)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 转换截图为灰度图像
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # 进行模板匹配
    result = cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # 计算点击位置
        template_height, template_width = template.shape
        click_x = max_loc[0] + template_width // 2
        click_y = max_loc[1] + template_height // 2
        return (click_x, click_y)

    else:
        print("未找到图像")


def text_in_str(text_arr=[], str=""):
    for text in text_arr:
        if text in str:
            return True
    return False


def text_diff(s1, s2, num=1):
    """根据两个字符串中相同字符出现的次数判断相似度"""
    counter1 = Counter(s1)
    counter2 = Counter(s2)
    common_characters = counter1 & counter2
    return sum(common_characters.values()) >= num


def is_mouse_in_center(tolerance=50):
    # 获取屏幕分辨率
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2

    # 获取当前鼠标位置
    current_x, current_y = pyautogui.position()

    # 判断鼠标是否在中心区域（考虑容差）
    if (center_x - tolerance <= current_x <= center_x + tolerance) and (
        center_y - tolerance <= current_y <= center_y + tolerance
    ):
        return True
    else:
        return False


def get_mouse_shape():
    # 获取鼠标光标形状
    cursor = win32gui.GetCursorInfo()
    cursor_shape = cursor[1]
    return cursor_shape


def game_status():
    return get_mouse_shape() == 0


if __name__ == "__main__":
    current_cursor = get_mouse_shape()
    print(f"当前鼠标形状: {current_cursor}")
    # 示例
    # string1 = "hello世界123"
    # string2 = "world你好123"
    # result = text_diff(string1, string2)
    # print(f": {result}")
