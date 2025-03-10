import win32gui
import win32con
import win32api
import time

# 初始化全局变量
text = "初始文字"
text_color = win32api.RGB(255, 255, 255)  # 白色文字
font_name = "微软雅黑"
font_size = 20


def draw_text():
    global text, text_color, font_name, font_size

    hwnd = win32gui.GetDesktopWindow()
    hdc = win32gui.GetDC(hwnd)

    # 定义字体属性
    lf = win32gui.LOGFONT()
    lf.lfHeight = font_size
    lf.lfWidth = 0
    lf.lfEscapement = 0
    lf.lfOrientation = 0
    lf.lfWeight = win32con.FW_NORMAL
    lf.lfItalic = 0
    lf.lfUnderline = 0
    lf.lfStrikeOut = 0
    lf.lfCharSet = win32con.ANSI_CHARSET
    lf.lfOutPrecision = win32con.OUT_DEFAULT_PRECIS
    lf.lfClipPrecision = win32con.CLIP_DEFAULT_PRECIS
    lf.lfQuality = win32con.ANTIALIASED_QUALITY
    lf.lfPitchAndFamily = win32con.DEFAULT_PITCH | win32con.FF_DONTCARE
    lf.lfFaceName = font_name

    # 创建字体
    font = win32gui.CreateFontIndirect(lf)

    # 保存原始字体
    old_font = win32gui.SelectObject(hdc, font)

    # 设置文字颜色
    win32gui.SetTextColor(hdc, text_color)

    # 设置文字背景透明
    win32gui.SetBkMode(hdc, win32con.TRANSPARENT)

    # 定义一个矩形区域（用于文字背景）
    rect = win32gui.RECT()
    rect.left = 100
    rect.top = 100
    rect.right = 100 + 100  # 假设文字宽度为100
    rect.bottom = 100 + 100  # 假设文字高度为100

    # 绘制文字
    win32gui.ExtTextOut(
        hdc, 100, 100, win32con.ETO_OPAQUE, rect, text, None
    )  # 在坐标 (100, 100) 绘制文字

    # 恢复原始字体
    win32gui.SelectObject(hdc, old_font)

    # 释放设备上下文
    win32gui.ReleaseDC(hwnd, hdc)


def update_text(new_text, new_color=None, new_font_name=None, new_font_size=None):
    global text, text_color, font_name, font_size
    text = new_text
    if new_color:
        text_color = new_color
    if new_font_name:
        font_name = new_font_name
    if new_font_size:
        font_size = new_font_size


def main_loop():
    while True:
        draw_text()
        time.sleep(1)  # 每隔1秒更新一次文字


# 示例使用
update_text(
    "更新后的文字", win32api.RGB(255, 0, 0), "楷体", 25
)  # 更新文字内容、颜色、字体和字号
main_loop()
