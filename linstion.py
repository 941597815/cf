import os
import winsound
from pynput import mouse, keyboard
from logitech_driver import Logitech
from osd import show_osd, hide_osd

alt_pressed = False


# 鼠标点击回调函数
def on_click(x, y, button, pressed, globals_instance):
    if button == mouse.Button.x1:  # 前进键
        if pressed:
            globals_instance.shandun = True
            if globals_instance.debug:
                print("闪蹲宏开始")
        else:
            globals_instance.shandun = False
            if globals_instance.debug:
                print("闪蹲宏结束")

    if button == mouse.Button.x2:
        if pressed:
            globals_instance.liantiao = True
            if globals_instance.debug:
                print("连跳宏开始")
        else:
            globals_instance.liantiao = False
            if globals_instance.debug:
                print("连跳宏结束")

    if button == mouse.Button.left:  # 检测鼠标左键
        if pressed:
            globals_instance.running = True
            globals_instance.mouseLeft = True
            if globals_instance.debug:
                print("炼狱宏开始")
        else:
            globals_instance.running = False
            globals_instance.mouseLeft = False
            if globals_instance.debug:
                print("炼狱宏结束")


# 鼠标监听器线程
def start_listener(globals_instance):
    listener = mouse.Listener(
        on_click=lambda x, y, button, pressed: on_click(
            x, y, button, pressed, globals_instance
        )
    )
    listener.start()
    listener.join()


def fn_keyboard_press(key, globals_instance):
    print(key, globals_instance)


def fn_keyboard_release(key, globals_instance):
    print(key, globals_instance)


def on_press(key, globals_instance):
    global alt_pressed
    # 检查按下的键是否是 Home 键
    if key == keyboard.Key.home:
        if globals_instance.debug:
            print("Home 键被按下")
        winsound.Beep(800, 100)
        winsound.Beep(600, 100)
        winsound.Beep(400, 100)
        os._exit(0)  # 结束程序
    if key == keyboard.Key.alt_l:
        alt_pressed = True

    if key == keyboard.Key.f5:
        globals_instance.weapons_identification = (
            not globals_instance.weapons_identification
        )
        if globals_instance.weapons_identification:
            winsound.Beep(800, 200)
            if globals_instance.debug:
                print("开始武器识别")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
            if globals_instance.debug:
                print("结束武器识别")

    if key == keyboard.Key.f6:
        globals_instance.cf.guaji = not globals_instance.cf.guaji
        globals_instance.cf.zhunbei = not globals_instance.cf.zhunbei
        if globals_instance.cf.guaji:
            winsound.Beep(800, 200)
            if globals_instance.debug:
                print("开始挂机")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
            if globals_instance.debug:
                print("结束挂机")

    if key == keyboard.Key.f7:
        globals_instance.auto_fire = not globals_instance.auto_fire
        if globals_instance.auto_fire:
            winsound.Beep(800, 200)
            if globals_instance.debug:
                print("自动开火打开")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
            if globals_instance.debug:
                print("自动开火关闭")

    if key == keyboard.Key.f8:
        globals_instance.osd = not globals_instance.osd
        if globals_instance.osd:
            winsound.Beep(800, 200)
            show_osd()
            if globals_instance.debug:
                print("OSD打开")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)
            hide_osd()
            if globals_instance.debug:
                print("OSD关闭")

    if alt_pressed and key == keyboard.KeyCode.from_char("j"):  # 狙击枪
        globals_instance.jujiqiang = not globals_instance.jujiqiang
        globals_instance.buqiang = False
        globals_instance.usp = False
        globals_instance.jtl = False
        if globals_instance.jujiqiang:
            winsound.Beep(800, 200)
            if globals_instance.debug:
                print("狙击枪模式")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

    if alt_pressed and key == keyboard.KeyCode.from_char("b"):  # 步枪
        globals_instance.buqiang = not globals_instance.buqiang
        globals_instance.jujiqiang = False
        globals_instance.usp = False
        globals_instance.jtl = False
        if globals_instance.buqiang:
            winsound.Beep(800, 200)
            if globals_instance.debug:
                print("步枪模式")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

    if alt_pressed and key == keyboard.KeyCode.from_char("l"):  # 炼狱
        globals_instance.jtl = not globals_instance.jtl
        globals_instance.jujiqiang = False
        globals_instance.buqiang = False
        globals_instance.usp = False
        if globals_instance.jtl:
            winsound.Beep(800, 200)
            if globals_instance.debug:
                print("炼狱模式")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

    if alt_pressed and key == keyboard.KeyCode.from_char("u"):  # usp
        globals_instance.usp = not globals_instance.usp
        globals_instance.jtl = False
        globals_instance.jujiqiang = False
        globals_instance.buqiang = False
        if globals_instance.usp:
            winsound.Beep(800, 200)
            if globals_instance.debug:
                print("USP模式")
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)


def on_release(key, globals_instance):
    global alt_pressed

    if key == keyboard.Key.alt_l:
        alt_pressed = False
        # print('altUp')


def start_keyboard(globals_instance):
    listener = keyboard.Listener(
        on_press=lambda key: on_press(key, globals_instance),
        on_release=lambda key: on_release(key, globals_instance),
    )
    listener.start()
    listener.join()
