from logitech_driver import Logitech
from random_delay import random_delay_ms
import time


def worker_macro(globals_instance):
    while True:
        if globals_instance.running and globals_instance.game_status:
            if globals_instance.jtl:
                if globals_instance.debug:
                    print("炼狱...")

                Logitech.keyboard.press(globals_instance.firebtn)
                random_delay_ms(91, 140)
                Logitech.keyboard.release(globals_instance.firebtn)
                random_delay_ms(14, 17)
            elif globals_instance.buqiang:
                if globals_instance.debug:
                    print("步枪...")

                if globals_instance.auto_fire:
                    Logitech.keyboard.press(globals_instance.firebtn)
                    random_delay_ms(30, 55)
                    Logitech.keyboard.release(globals_instance.firebtn)
                    random_delay_ms(32, 55)
                    # Logitech.mouse.move(x=0, y=2)
                else:
                    Logitech.keyboard.press(globals_instance.firebtn)
                    random_delay_ms(30, 65)
            elif globals_instance.jujiqiang:
                if globals_instance.debug:
                    print("狙击枪...")

                if globals_instance.auto_fire:
                    if globals_instance.auto_fire_openScope:
                        Logitech.mouse.click(2)
                        random_delay_ms(50, 70)
                    Logitech.keyboard.click(globals_instance.firebtn)
                    random_delay_ms(50, 80)
                else:
                    Logitech.keyboard.press(globals_instance.firebtn)
                    random_delay_ms(40, 60)
                    Logitech.keyboard.release(globals_instance.firebtn)
                    random_delay_ms(14, 30)

            elif globals_instance.usp:
                if globals_instance.debug:
                    print("USP...")

                Logitech.keyboard.press(globals_instance.firebtn)
                random_delay_ms(30, 50)
                Logitech.keyboard.release(globals_instance.firebtn)
                random_delay_ms(22, 30)
                if globals_instance.auto_fire:
                    Logitech.mouse.move(x=0, y=2)

        # if globals_instance.shandun:
        #     Logitech.keyboard.click_('ctrl')
        #     random_delay_ms(35,50)
        # if globals_instance.liantiao:
        #     Logitech.keyboard.click_('space')
        #     random_delay_ms(35,50)
        else:
            time.sleep(0.008)  # 降低 CPU 使用率
            if globals_instance.buqiang and not globals_instance.auto_fire:
                Logitech.keyboard.release(globals_instance.firebtn)
