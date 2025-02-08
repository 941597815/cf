import threading
from osd import OSD
import time
import queue

# 创建一个线程安全的队列，用于在主线程和子线程之间传递消息
q = queue.Queue()

def osd_start():
    # 创建 HoverLabel 实例
    osd = OSD(
        text="0",
        font=("Arial", 14),
        fg="red",
        bg="black",
    )
    osd.show()

    # 主线程通过队列传递更新文本的请求
    def update_text_loop():
        while True:
            # 检查队列中是否有新的文本更新请求
            if not q.empty():
                new_text = q.get()
                osd.update_text(new_text)
            time.sleep(0.1)  # 适当的时间间隔，避免频繁检查队列

    # 在另一个线程中运行 update_text_loop，避免阻塞主线程和 OSD 主循环
    update_thread = threading.Thread(target=update_text_loop)
    update_thread.daemon = True
    update_thread.start()

    # 运行 OSD 的主循环（假设 `run` 是一个阻塞方法）
    osd.run()

# 创建线程
thread_osd = threading.Thread(target=osd_start)

# 启动线程
thread_osd.start()

i = 0
while True:
    time.sleep(1)
    i += 1
    # 将新的文本通过队列传递给子线程中的 OSD 对象
    q.put(str(i))