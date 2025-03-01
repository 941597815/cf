from pynput import mouse,keyboard
import os
from logitech_driver import Logitech
import winsound

alt_pressed = False

def fn_mouse(pressed,globals_instance):
    if pressed and globals_instance.jtl:
        globals_instance.running = True
        
    else:
        globals_instance.running = False



# 鼠标点击回调函数
def on_click(x, y, button, pressed, globals_instance):
    # if button == mouse.Button.x1:  # 前进键
    #     fn(pressed,globals_instance)
    # if button == mouse.Button.x2:  # 前进键
    #     fn(pressed,globals_instance)
    if button == mouse.Button.left:  # 检测鼠标左键
        fn_mouse(pressed,globals_instance)

# 鼠标监听器线程
def start_listener(globals_instance):
    listener = mouse.Listener(on_click=lambda x, y, button, pressed: on_click(x, y, button, pressed, globals_instance))
    listener.start()
    listener.join()


def fn_keyboard_press(key,globals_instance):
    print(key,globals_instance)
    
def fn_keyboard_release(key,globals_instance):
    print(key,globals_instance)

def on_press(key,globals_instance):
    global alt_pressed
    # 检查按下的键是否是 Home 键
    if key == keyboard.Key.home:
        print("Home 键被按下")
        winsound.Beep(800, 100)
        winsound.Beep(600, 100)
        winsound.Beep(400, 100)
        os._exit(0)  # 结束程序
    if key == keyboard.Key.alt_l:
        alt_pressed = True

    if key == keyboard.Key.f6:
        globals_instance.cf.guaji=not globals_instance.cf.guaji
        globals_instance.cf.zhunbei=not globals_instance.cf.zhunbei
        if(globals_instance.cf.guaji):
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

    if key == keyboard.Key.f7:
        globals_instance.auto_fire=not globals_instance.auto_fire
        if(globals_instance.auto_fire):
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

    if alt_pressed and key == keyboard.KeyCode.from_char('j'):#狙击枪
        globals_instance.jujiqiang=not globals_instance.jujiqiang
        globals_instance.buqiang=False
        # globals_instance.jtl=False
        if(globals_instance.jujiqiang):
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

    if alt_pressed and key == keyboard.KeyCode.from_char('b'):#步枪
        globals_instance.buqiang=not globals_instance.buqiang
        globals_instance.jujiqiang=False
        # globals_instance.jtl=False
        if(globals_instance.buqiang):
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

    if alt_pressed and key == keyboard.KeyCode.from_char('l'):#炼狱
        globals_instance.jtl=not globals_instance.jtl
        globals_instance.jujiqiang=False
        globals_instance.buqiang=False
        if(globals_instance.jtl):
            winsound.Beep(800, 200)
        else:
            winsound.Beep(800, 100)
            winsound.Beep(600, 100)

def on_release(key,globals_instance):
    global alt_pressed

    if key == keyboard.Key.alt_l:
        alt_pressed = False
        # print('altUp')

    
    
    
    

def start_keyboard(globals_instance):
    listener = keyboard.Listener(on_press=lambda key: on_press(key, globals_instance),on_release=lambda key: on_release(key, globals_instance))
    listener.start()
    listener.join()