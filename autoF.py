import mss
import numpy as np
import time
from ocr import getImgText  # 假设 getImgText 函数定义在 ocr.py 文件中
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

    # 调用 getImgText 函数识别文字
    recognized_text = getImgText(image)

    print("识别结果：", recognized_text)
    if(recognized_text):
        Logitech.mouse.click(1)
    return recognized_text

if __name__ == "__main__":
    # 设置截图区域和间隔
    # bounding_box = (1650, 940, 1900, 1000)
    bounding_box = (900, 590, 1020, 625)
    while True:
      custom_screenshot(bounding_box)
      # time.sleep(0.01)
        

    