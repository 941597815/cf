import ctypes
import os
import pyautogui

# import time

try:
    root = os.path.abspath(os.path.dirname(__file__))
    driver = ctypes.CDLL(f"{root}/logitech_driver.dll")
    ok = driver.device_open() == 1  # 该驱动每个进程可打开一个实例
    if not ok:
        print("Error, GHUB or LGS driver not found")
except FileNotFoundError:
    print(f"Error, DLL file not found")


class Logitech:

    class mouse:
        """
        code: 1:左键, 2:中键, 3:右键
        """

        @staticmethod
        def press(code):
            if not ok:
                return
            driver.mouse_down(code)

        @staticmethod
        def release(code):
            if not ok:
                return
            driver.mouse_up(code)

        @staticmethod
        def click(code):
            if not ok:
                return
            driver.mouse_down(code)
            driver.mouse_up(code)

        @staticmethod
        def scroll(a):
            """
            a:没搞明白
            """
            if not ok:
                return
            driver.scroll(a)

        @staticmethod
        def move(x, y):
            """
            相对移动, 绝对移动需配合 pywin32 的 win32gui 中的 GetCursorPos 计算位置
            pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple
            x: 水平移动的方向和距离, 正数向右, 负数向左
            y: 垂直移动的方向和距离
            """
            if not ok:
                return
            if x == 0 and y == 0:
                return
            driver.moveR(x, y, True)

        def moveto(x, y, duration=1):
            pyautogui.moveTo(x, y, duration)

            # if not ok:
            #     return
            # if x == 0 and y == 0:
            #     return
            # sleep_time = round(d / max(abs(x - current_x), abs(y - current_y)), 3)
            # current_x, current_y = win32gui.GetCursorPos()
            # while current_x != x or current_y != y:
            #     current_x, current_y = win32gui.GetCursorPos()
            #     # print(current_x, current_y)
            #     dx = x - current_x
            #     dy = y - current_y
            #     # 计算方向
            #     direction_x = 1 if dx > 0 else (-1 if dx < 0 else 0)
            #     direction_y = 1 if dy > 0 else (-1 if dy < 0 else 0)
            #     # 调用移动方法
            #     driver.moveR(direction_x, direction_y, True)
            #     time.sleep(0.001)

    class keyboard:
        """
        键盘按键函数中，传入的参数采用的是键盘按键对应的键码
        code:a-z 0-9 f1-f24 enter esc back_space tab space minus equal square_bracket_left square_bracket_right back_slash back_slash_  column  quote  back_tick  comma  period  slash  cap printscreen  scroll_lock  pause  insert  home  page_up  del  end  page_down  right  left  down  up  numlock  numpad_div  numpad_mul  numpad_minus  numpad_plus   numpad_enter  numpad_1  numpad_2  numpad_3  numpad_4  numpad_5  numpad_6  numpad_7  numpad_8  numpad_9  numpad_0  numpad_dec  apps  lctrl  lshift  lalt  lwin  rctrl  rshift  ralt
        """

        @staticmethod
        def press(code):

            if not ok:
                return
            driver.key_down(code.encode("utf-8"))

        @staticmethod
        def release(code):
            if not ok:
                return
            driver.key_up(code.encode("utf-8"))

        @staticmethod
        def click(code):
            if not ok:
                return
            driver.key_down(code.encode("utf-8"))
            driver.key_up(code.encode("utf-8"))


if __name__ == "__main__":
    # Logitech.keyboard.click("space")
    Logitech.mouse.moveto(1000, 100)
