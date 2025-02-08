from pynput import mouse
from logitech_driver import Logitech
from random_delay import random_delay_ms
import time

import threading


# 定义全局变量
running = False
isApi=False

# 鼠标点击回调函数
def on_click(x, y, button, pressed):
    global running,isApi
    if button == mouse.Button.x1:  # 前进键
        if pressed:
            print("前进键按下，启动循环")
            running = True
        else:
            print("前进键释放，停止循环")
            running = False
    # if button == mouse.Button.left:  # 检测鼠标左键
    #     if pressed and (not isApi) and not running:
    #         print("鼠标左键按下，启动循环")
    #         running = True
    #     else:
    #         if not isApi:
    #           ("鼠标左键释放，停止循环")
    #           running = False


# 鼠标监听器线程
def start_listener():
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()

# 主任务线程
def main_task():
    global running,isApi
    while True:
        if running:
            print("循环中...")
            Logitech.mouse.press(1)
            random_delay_ms(101,150)
            Logitech.mouse.release(1)
            random_delay_ms(15,17)
        else:
            time.sleep(0.1)  # 降低 CPU 使用率

# 启动监听器线程
listener_thread = threading.Thread(target=start_listener)
listener_thread.daemon = True  # 设置为守护线程
listener_thread.start()

# 启动主任务线程
main_thread = threading.Thread(target=main_task)
main_thread.start()




