from pynput import mouse
import time
import threading
from logitech_driver import Logitech
from random_delay import random_delay_ms
from linstion import start_listener,start_keyboard
from cf import worker_CF,worker_CF_zb
from autoF import worker_auto_fire
from globals import globals_instance
# from ocr import worker_ocr


# 主任务线程
def main_task():
    while True:
        if globals_instance.running:
                print("循环中...")
                # Logitech.mouse.press(1)
                Logitech.keyboard.press(globals_instance.firebtn)
                random_delay_ms(101,150)
                # Logitech.mouse.release(1)
                Logitech.keyboard.release(globals_instance.firebtn)
                random_delay_ms(15,17)
        else:
            time.sleep(0.008)  # 降低 CPU 使用率
    

# 启动监听器线程p
listener_mouse_thread = threading.Thread(target=start_listener,args=(globals_instance,),daemon=True).start()
listener_keyboard_thread = threading.Thread(target=start_keyboard,args=(globals_instance,),daemon=True).start()
# ocr_thread = threading.Thread(target=worker_ocr,args=(globals_instance,),daemon=True).start()
listener_CF_thread = threading.Thread(target=worker_CF,args=(globals_instance,),daemon=True).start()
listener_CF_zb_thread = threading.Thread(target=worker_CF_zb,args=(globals_instance,),daemon=True).start()
listener_autoFire_thread = threading.Thread(target=worker_auto_fire,args=(globals_instance,),daemon=True).start()


# 启动主任务线程
main_thread = threading.Thread(target=main_task)
main_thread.start()



