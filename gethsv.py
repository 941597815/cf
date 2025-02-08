import cv2
import numpy as np

hsv = cv2.cvtColor(np.uint8([[b, g, r]]), cv2.COLOR_BGR2HSV)[0][0]
print(f"HSV值: H={hsv[0]}, S={hsv[1]}, V={hsv[2]}")
# 鼠标回调函数
def get_pixel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 鼠标左键点击
        # 获取BGR颜色
        b, g, r = param[y, x]
        # 转换为HSV
        hsv = cv2.cvtColor(np.uint8([[b, g, r]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"HSV值: H={hsv[0]}, S={hsv[1]}, V={hsv[2]}")
