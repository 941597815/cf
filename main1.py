import mss
import numpy as np
import time
from ocr import getImgText  # 假设 getImgText 函数定义在 ocr.py 文件中
import tkinter as tk
from PIL import Image, ImageTk
import threading
from queue import Queue

# 初始化窗口
root = tk.Tk()
root.overrideredirect(True)  # 去掉窗口边框
root.geometry("+0+0")  # 窗口位置设为屏幕左上角
root.attributes("-alpha", 0.5)  # 窗口透明度
root.attributes("-topmost", True)  # 窗口置顶

# 创建一个队列用于线程间通信
result_queue = Queue()

# 创建一个标签用于显示文字
label = tk.Label(root, text="", font=('Arial', 14), bg='white', fg='black')
label.pack(pady=20)

def custom_screenshot(bounding_box=None):
    """
    截图并识别文字。

    参数:
        bounding_box: 截图区域的边界框，格式为 (left, top, right, bottom)。

    返回:
        识别出的文字。
    """
    # 使用 mss 截图
    with mss.mss() as sct:
        # 获取屏幕上的第一个显示器信息
        if bounding_box:
            monitor = bounding_box
        else:
            monitor = sct.monitors[0]

        # 捕获屏幕截图
        screenshot = sct.grab(monitor)

        # 将截图转换为 numpy 数组并转换为 RGB 格式
        image = np.array(screenshot)[:, :, :3]  # 去掉透明通道（A），只保留 RGB

    # 调用 getImgText 函数识别文字
    recognized_text = getImgText(image)

    print("识别结果：", recognized_text)
    return recognized_text

def worker_thread(bounding_box, delay):
    """
    工作线程，负责持续截图和 OCR 识别。
    """
    while True:
        text = custom_screenshot(bounding_box)
        # 将结果放入队列中
        result_queue.put(text)
        time.sleep(delay)

def update_text():
    """
    定期从队列中取出结果并更新标签。
    """
    try:
        # 尝试从队列中获取结果
        text = result_queue.get_nowait()
        label.config(text=text)
        # 标记任务完成
        result_queue.task_done()
    except:
        # 如果队列为空，忽略错误
        pass

    # 每隔一定时间检查队列
    root.after(500, update_text)

if __name__ == "__main__":
    # 设置截图区域和间隔
    # bounding_box = (1650, 940, 1900, 1000)
    bounding_box = (1650, 940, 1900, 1000)
    delay = 0.5  # 1.5 秒间隔

    # 启动工作线程
    threading.Thread(target=worker_thread, args=(bounding_box, delay), daemon=True).start()

    # 启动定时任务更新标签
    root.after(500, update_text)

    # 运行主事件循环
    root.mainloop()