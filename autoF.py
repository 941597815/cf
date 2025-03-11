import cv2
import time

from logitech_driver import Logitech
from random_delay import random_delay_ms
from utils import (
    game_dict,
    custom_screenshot,
    save_image,
    hsv_value,
    color_similarity_rgb,
)


def is_red(hsv, min_s=50, min_v=50):
    h, s, v = hsv
    # 检查色相是否在红色区间
    red_low = (h >= 0) and (h <= 15)
    red_high = (h >= 165) and (h <= 180)
    # 检查饱和度和明度是否足够
    return (red_low or red_high) and (s >= min_s) and (v >= min_v)


def check_pixel_surrounding_for_imgpath(
    image_input, target_rgb1, target_rgb2, similarity_threshold=1
):
    img = cv2.imread(image_input)
    check_pixel_surrounding(img, target_rgb1, target_rgb2, similarity_threshold)


def check_pixel_surrounding(rgb_img, target_rgb1, target_rgb2, similarity_threshold=1):
    """
    检查图片中是否存在符合规则的像素点.

    参数:
        rgb_img: 图片的 NumPy 数组格式的图像 (RGB 格式).
        target_rgb1: 第一种目标 RGB 颜色值，如 (0, 0, 0) 代表黑色.
        target_rgb2: 第二种目标 RGB 颜色值，如 (242, 74, 23).
        similarity_threshold: 颜色相似度阈值（0 到 1，0 表示最不相似，1 表示完全相同）.

    返回:
        是否存在符合规则的像素点.
    """

    height, width, _ = rgb_img.shape

    # 遍历图像中的每个像素
    for y in range(height):
        for x in range(width):
            current_pixel = rgb_img[y, x]
            # 判断当前点是否在红色范围内
            if not is_red(hsv_value(current_pixel)):
                continue
            # 检查当前像素相似度是否满足
            if color_similarity_rgb(target_rgb2, current_pixel) >= similarity_threshold:
                # 收集上下左右四个相邻像素
                neighbors = []
                # 上
                if y > 0:
                    neighbors.append(rgb_img[y - 1, x])
                # 下
                if y < height - 1:
                    neighbors.append(rgb_img[y + 1, x])
                # 左
                if x > 0:
                    neighbors.append(rgb_img[y, x - 1])
                # 右
                if x < width - 1:
                    neighbors.append(rgb_img[y, x + 1])
                # print(neighbors,target_rgb1,target_rgb2)
                # 检查邻居像素是否至少包含一个 target_rgb1 和至少一个 target_rgb2
                has_target1 = any(
                    (neighbor == target_rgb1).all() for neighbor in neighbors
                )
                has_target2 = any(
                    (neighbor == current_pixel).all() for neighbor in neighbors
                )
                if has_target1 and has_target2:
                    # print(color_similarity_rgb(target_rgb2,current_pixel),current_pixel,target_rgb2)
                    # # 保存截图
                    # save_image(rgb_img, "redName.png")
                    # print(f"符合条件的像素p点位于 (x={x}, y={y})")
                    return True  # 找到一个符合条件的像素点，返回 True

    # print("未找到符合条件的像素点")
    return False


def autoFire(globals_instance):
    bounding_box = game_dict[globals_instance.resolution]["red_name_box"]
    rgb = (0, 0, 0)
    # 红名变化范围
    # rgb_b = (242, 74, 23)
    # rgb_c = (177, 60, 45)
    # rgb_d = (160, 57, 50)
    # rgb_e = (154, 55, 52)
    rgb_Center = (198, 65, 38)

    image = custom_screenshot(bounding_box)
    isFire = check_pixel_surrounding(
        image, rgb, rgb_Center, globals_instance.similarity
    )
    if isFire:
        random_delay_ms(globals_instance.fireDelay, globals_instance.fireDelay + 10)
        globals_instance.running = True
        # if globals_instance.jujiqiang:
        #     print("jujiqiang")
        #     Logitech.mouse.click(2)
        #     random_delay_ms(50, 70)
        #     Logitech.keyboard.click(globals_instance.firebtn)
        #     random_delay_ms(50, 80)

        # elif globals_instance.buqiang:
        #     Logitech.keyboard.click(globals_instance.firebtn)
        #     random_delay_ms(3, 15)
        #     Logitech.mouse.move(x=0, y=2)

        # elif globals_instance.usp:
        #     Logitech.keyboard.press(globals_instance.firebtn)
        #     random_delay_ms(40, 60)
        #     Logitech.keyboard.release(globals_instance.firebtn)
        #     random_delay_ms(14, 30)
        #     Logitech.mouse.move(x=0, y=1)

        # Logitech.keyboard.press(globals_instance.firebtn)
        # random_delay_ms(10,20)
        # Logitech.keyboard.release(globals_instance.firebtn)
        # print('开火')
    else:
        if not globals_instance.mouseLeft and globals_instance.running:
            globals_instance.running = False


def worker_auto_fire(globals_instance):
    while True:
        if globals_instance.auto_fire:
            autoFire(globals_instance)
        else:
            time.sleep(1)
