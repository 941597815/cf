import tkinter as tk
import win32gui
import win32con
import pywintypes

class OSD:
    def __init__(self, text, font, fg="black", bg="white"):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # 隐藏边框
        self.root.lift()  # 提升窗口层级
        self.root.wm_attributes("-topmost", True)  # 置顶
        self.root.wm_attributes("-transparentcolor", bg)  # 设置透明颜色
        self.root.configure(bg=bg)  # 设置背景颜色

        self.label = tk.Label(self.root, text=text, font=font, fg=fg, bg=bg)
        self.label.pack(padx=10, pady=10)  # 设置内边距

        self._set_window_style()

        # 将窗口隐藏
        self.root.withdraw()

    def _set_window_style(self):
        """设置窗口样式"""
        hwnd = pywintypes.HANDLE(int(self.root.frame(), 16))
        ex_style = (
            win32con.WS_EX_COMPOSITED |
            win32con.WS_EX_LAYERED |
            win32con.WS_EX_NOACTIVATE |
            win32con.WS_EX_TOPMOST |
            win32con.WS_EX_TRANSPARENT
        )
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    def show(self):
        """显示窗口"""
        self.root.deiconify()

    def hide(self):
        """隐藏窗口"""
        self.root.withdraw()

    def update_text(self, new_text):
        """更新文字内容"""
        self.label.config(text=new_text)

    def run(self):
        """运行窗口主循环"""
        self.root.mainloop()

    def update(self):
        """更新窗口"""
        self.root.update()