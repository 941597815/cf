from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import time
import mss


# 初始化 PaddleOCR
ocr = PaddleOCR(use_angle_cls=False, lang="ch")  # 关闭角度分类器，使用中文识别

def getImgText(img):
    """
    使用 PaddleOCR 识别图片中的文字。
    
    参数:
        img: 图片路径（字符串）或 Pillow 图像对象。
    
    返回:
        识别出的文本字符串。
    """
    
    try:
        # 判断输入是路径还是 Pillow 图像对象
        if isinstance(img, str):
            # 如果是路径，打开图像并转换为 numpy 数组
            image = np.array(Image.open(img).convert('RGB'))
        else:
            image=img
        # elif isinstance(img, Image.Image):
        #     # 如果是 Pillow 图像对象，直接转换为 numpy 数组
        #     image = np.array(img.convert('RGB'))
        # else:
        #     raise ValueError("Unsupported image format. Please provide a path or a Pillow Image object.")
        # 记录开始时间
        # start_time = time.time()
        # 执行 OCR 识别
        result = ocr.ocr(image, cls=False)
        # 记录结束时间
        # end_time = time.time()
        # 计算耗时
        # elapsed_time = end_time - start_time
        # print(f"代码运行耗时: {elapsed_time:.6f} 秒")
        # 提取识别文字
        # text = ''.join([line[1][0] for line in result])
        text=''
        # 遍历识别结果并提取文字
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                # print(line)
                text+=line[1][0]
        return text

    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    

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

def isJtl():
    1
    

def worker_ocr(globals_instance):
    # bounding_box = (1650, 940, 1900, 1000)  #1920x1080
    bounding_box = (1410, 800, 1590, 830)  #1600x900
    while True:
        text=custom_screenshot(bounding_box)
        if text:
            # 判断是否包含“炼狱”
            if "炼狱" in text:
                print("文本中包含“炼狱”")
                globals_instance.jtl=True
            else:
                print("文本中不包含“炼狱”")
                globals_instance.jtl=False

            time.sleep(2.5)
        else:
            time.sleep(5)