# main.py
from logitech_driver import Logitech
import time

def test_mouse():
    # 点击鼠标左键
    Logitech.mouse.click(1)
    time.sleep(1)
    # 点击鼠标右键
    Logitech.mouse.click(3)
    time.sleep(1)
    # 滚动鼠标滚轮
    Logitech.mouse.scroll(1)  # 向上滚动
    Logitech.mouse.scroll(-1) # 向下滚动
    time.sleep(1)
    # 移动鼠标
    Logitech.mouse.move(10, 10)  # 向右下角移动 10 个单位

def test_keyboard():
    # 按下并释放键盘按键
    Logitech.keyboard.press('a')
    Logitech.keyboard.release('a')
    # 点击键盘按键
    Logitech.keyboard.click('a')
    
if __name__ == "__main__":
    test_mouse()
    # test_keyboard()