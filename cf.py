from logitech_driver import Logitech
from random_delay import random_delay_ms
import time
import pyautogui


class CF:
    class guaji:

        def yd(globals_instance):
            # Logitech.keyboard.press('w')
            # random_delay_ms(500,1500)
            # Logitech.keyboard.release('w')
            # # Logitech.keyboard.press('d')
            # # random_delay_ms(500,1500)
            # # Logitech.keyboard.release('d')
            # Logitech.keyboard.press('s')
            # random_delay_ms(500,1500)
            # Logitech.keyboard.release('s')
            # # Logitech.keyboard.press('a')
            # # random_delay_ms(500,1500)
            # # Logitech.keyboard.release('a')
            Logitech.keyboard.click("e")
            Logitech.keyboard.click("f")
            # pyautogui.keyDown('f11')
            # pyautogui.keyUp('f11')
            Logitech.keyboard.click("2")
            # Logitech.keyboard.click('p')

            random_delay_ms(900, 2800)

        def zhubei(globals_instance):
            i = 1
            if globals_instance.resolution == 2:
                i = 1920 / 1600
            elif globals_instance.resolution == 3:
                i = 2560 / 1600

            # Logitech.mouse.moveto(x=-100,y=1)
            Logitech.mouse.moveto(830 * i, 770 * i)  # 推荐装备关闭
            pyautogui.click()
            random_delay_ms(100, 300)
            Logitech.mouse.moveto(800 * i, 550 * i)  # 未满足最低任务条件，确认键
            pyautogui.click()
            random_delay_ms(100, 300)
            Logitech.mouse.moveto(880 * i, 608 * i)  # 每日任务，关闭键
            pyautogui.click()
            random_delay_ms(100, 300)
            Logitech.mouse.moveto(1475 * i, 660 * i)  # 准备
            pyautogui.click()
            random_delay_ms(10000, 20000)


def worker_CF(globals_instance):
    # i=0

    while True:
        if globals_instance.cf.guaji:
            # i+=1
            # print(f"正在挂机移动{i}")
            CF.guaji.yd(globals_instance)

        else:
            i = 0
            time.sleep(0.1)


def worker_CF_zb(globals_instance):
    while True:
        if globals_instance.cf.zhunbei and not globals_instance.game_status:
            CF.guaji.zhubei(globals_instance)
        else:
            time.sleep(3)


if __name__ == "__main__":
    CF.guaji.zhubei()
