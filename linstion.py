from pynput import mouse,keyboard
import os
from logitech_driver import Logitech
from cf import CF
import winsound
import time

def fn(pressed,globals_instance):
    if pressed:
        if globals_instance.jtl:
            globals_instance.running = True
        else:
            Logitech.keyboard.press(globals_instance.firebtn)
    else:
        if globals_instance.jtl:
            globals_instance.running = False
        else:
            Logitech.keyboard.release(globals_instance.firebtn)

# 鼠标点击回调函数
def on_click(x, y, button, pressed, globals_instance):
    if button == mouse.Button.x1:  # 前进键
        fn(pressed,globals_instance)
    if button == mouse.Button.x2:  # 前进键
        fn(pressed,globals_instance)
    if button == mouse.Button.left:  # 检测鼠标左键
        fn(pressed,globals_instance)

# 鼠标监听器线程
def start_listener(globals_instance):
    listener = mouse.Listener(on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, globals_instance))
    listener.start()
    listener.join()



def on_press(key,globals_instance):
    try:
        # 检查按下的键是否是 Home 键
        if key == keyboard.Key.home:
            print("Home 键被按下")
    except AttributeError:
        pass  # 忽略特殊键（如 Shift、Ctrl 等）

def on_release(key,globals_instance):
    # 检查释放的键是否是 Home 键
    if key == keyboard.Key.home:
        print("Home 键被释放")
        # Logitech.keyboard.release(globals_instance.firebtn)
        os._exit(0)  # 结束程序
    # # 如果按下 Esc 键，则停止监听
    if key == keyboard.Key.f6:
        globals_instance.cf.guaji=not globals_instance.cf.guaji
        globals_instance.cf.zhunbei=not globals_instance.cf.zhunbei
        if(globals_instance.cf.guaji):
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
    # if key == keyboard.Key.f6:
    #     CF.guaji.zhubei()

def start_keyboard(globals_instance):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, globals_instance),on_release=lambda key: on_release(key, globals_instance))
    listener.start()
    listener.join()