import tkinter as tk
from ctypes import windll
import time

on_color = "red"
off_color = "#ffffff"
root = None
label_gameStatus = tk.Label()
label_gameStatus_ = tk.Label()
label_autoFire = tk.Label()
label_autoFire_ = tk.Label()
label_wuqishibie = tk.Label()
label_wuqishibie_ = tk.Label()
label_wuqimoshi = tk.Label()
label_wuqimoshi_ = tk.Label()
label_autoZb = tk.Label()
label_autoZb_ = tk.Label()
label_debug = tk.Label()
label_debug_ = tk.Label()


def creatOSD(globals_instance):
    global root, on_color, off_color, label_gameStatus, label_gameStatus_, label_autoFire, label_autoFire_, label_wuqishibie, label_wuqishibie_, label_wuqimoshi, label_wuqimoshi_, label_autoZb, label_autoZb_, label_debug, label_debug_
    root = tk.Tk()
    root.overrideredirect(True)  # 移除窗口边框
    root.geometry("+10+4")  # 设置窗口位置（距左上角x=20,y=40）
    root.attributes("-topmost", True)  # 置顶显示

    # 设置透明背景
    root.config(bg="#000000")  # 使用特殊颜色值作为透明色
    root.attributes("-transparentcolor", "#000000")
    # 创建文字标签
    label_gameStatus = tk.Label(
        root,
        text="游戏状态:",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_gameStatus_ = tk.Label(
        root,
        text="",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_wuqishibie = tk.Label(
        root,
        text="武器识别(F5):",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_wuqishibie_ = tk.Label(
        root,
        text="",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_wuqimoshi = tk.Label(
        root,
        text="武器模式(Alt+B/J/L/U):",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_wuqimoshi_ = tk.Label(
        root,
        text="",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_autoZb = tk.Label(
        root,
        text="自动准备(F6):",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_autoZb_ = tk.Label(
        root,
        text="",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_autoFire = tk.Label(
        root,
        text="自动开火(F7):",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_autoFire_ = tk.Label(
        root,
        text="",
        font=(12),
        fg=off_color,
        bg="#000000",
    )
    label_debug = tk.Label(
        root,
        text="DEBUG",
        font=(12),
        fg=on_color,
        bg="#000000",
    )
    label_debug_ = tk.Label(
        root,
        text="",
        font=(12),
        fg=off_color,
        bg="#000000",
    )

    label_gameStatus.pack(side="left")
    label_gameStatus_.pack(side="left", padx=(0, 10))
    label_wuqishibie.pack(side="left")
    label_wuqishibie_.pack(side="left", padx=(0, 10))
    label_wuqimoshi.pack(side="left")
    label_wuqimoshi_.pack(side="left", padx=(0, 10))
    label_autoZb.pack(side="left")
    label_autoZb_.pack(side="left", padx=(0, 10))
    label_autoFire.pack(side="left")
    label_autoFire_.pack(side="left", padx=(0, 10))
    # label_debug.pack(side="left")
    # label_debug_.pack(side="left", padx=(0, 10))

    # label = tk.Label(
    #     root, text="文字", font=(12), fg="red", bg="#000000"
    # )  # 背景色与透明色一致
    # label.pack()
    # 设置窗口点击穿透
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, -20)  # GWL_EXSTYLE
    style |= 0x00080000  # WS_EX_LAYERED
    style |= 0x00000020  # WS_EX_TRANSPARENT
    windll.user32.SetWindowLongPtrW(hwnd, -20, style)
    if not globals_instance.osd:
        root.withdraw()
    root.mainloop()


def updata_osd(globals_instance, txt=""):
    global off_color, on_color

    text = ""
    fg = off_color

    # 游戏状态
    if globals_instance.game_status:
        text = "游戏中"
        fg = on_color
    else:
        text = "未开始"
        fg = off_color
    label_gameStatus_.config(text=text, fg=fg)

    # 武器识别
    if globals_instance.weapons_identification:
        text = "开"
        fg = on_color
    else:
        text = "关"
        fg = off_color
    label_wuqishibie_.config(text=text, fg=fg)

    # 武器模式
    fg = on_color
    if globals_instance.jujiqiang:
        text = "狙击枪"
    elif globals_instance.jtl:
        text = "加特林"
    elif globals_instance.usp:
        text = "USP"
    elif globals_instance.buqiang:
        text = "步枪"
    else:
        text = "--"
        fg = off_color
    label_wuqimoshi_.config(text=text, fg=fg)

    # 自动准备
    if globals_instance.cf.zhunbei:
        text = "开"
        fg = on_color
    else:
        text = "关"
        fg = off_color
    label_autoZb_.config(text=text, fg=fg)

    # 自动开火
    if globals_instance.auto_fire:
        text = "开"
        fg = on_color
    else:
        text = "关"
        fg = off_color
    label_autoFire_.config(text=text, fg=fg)

    # if globals_instance.debug:
    #     label_debug.pack()
    #     label_debug_.pack()
    #     if txt:
    #         label_debug_.config(text=txt)


def updata_osd_debug(text=""):
    if text:
        label_debug.config(text=text)


def show_osd():
    root.deiconify()


def hide_osd():
    root.withdraw()


# def worker_osd(globals_instance):
