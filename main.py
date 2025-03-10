import threading
import time
from globals import globals_instance
from linstion import start_listener, start_keyboard
from cf import worker_CF, worker_CF_zb
from autoF import worker_auto_fire
from macro import worker_macro
from ocr import worker_ocr
from osd import creatOSD, updata_osd
from utils import game_status

# from ui import start_ui

# 启动监听器线程
listener_mouse_thread = threading.Thread(
    target=start_listener, args=(globals_instance,), daemon=True
).start()
listener_keyboard_thread = threading.Thread(
    target=start_keyboard, args=(globals_instance,), daemon=True
).start()
listener_ocr_thread = threading.Thread(
    target=worker_ocr, args=(globals_instance,), daemon=True
).start()
listener_osd_thread = threading.Thread(
    target=creatOSD, args=(globals_instance,), daemon=True
).start()
listener_macro_thread = threading.Thread(
    target=worker_macro, args=(globals_instance,), daemon=True
).start()
listener_CF_thread = threading.Thread(
    target=worker_CF, args=(globals_instance,), daemon=True
).start()
listener_CF_zb_thread = threading.Thread(
    target=worker_CF_zb, args=(globals_instance,), daemon=True
).start()
listener_autoFire_thread = threading.Thread(
    target=worker_auto_fire, args=(globals_instance,), daemon=True
).start()

if __name__ == "__main__":
    print("启动完成")
    while True:
        globals_instance.game_status = game_status()
        if globals_instance.osd:
            updata_osd(globals_instance)
        time.sleep(0.1)
