from paddleocr import PaddleOCR

# import psutil
# import os

# 初始化 PaddleOCR
OCR = PaddleOCR(
    lang="ch",
    use_mp=True,
    show_log=False,
    det_model_dir="./ocrMode/v4/det",  # 文本检测模型
    rec_model_dir="./ocrMode/v4/rec",  # 文本识别模型
)  # 使用中文识别,开启多进程预测,关闭日志


# 获取当前进程的 PID
# pid = os.getpid()
# process = psutil.Process(pid)
# 设置 CPU 亲和性（限制进程可以使用的 CPU 核心）
# process.cpu_affinity(
#     [
#         0,
#     ]
# )  # 限制进程只能使用 CPU 核心 0
# 获取当前进程的 CPU 亲和性
# print(f"CPU 亲和性: {process.cpu_affinity()}")


def getImgText(image):
    """
    使用 PaddleOCR 识别图片中的文字。

    参数:
        img: 图片路径（字符串）或 Pillow 图像对象。

    返回:
        识别出的文本字符串。
    """
    # try:

    # 执行 OCR 识别
    result = OCR.ocr(image, cls=False)
    # print(result, result == None, result[0], result[0] == None)
    if result[0] == None:
        return None
    text = ""
    # 遍历识别结果并提取文字p
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            # print(line)
            text += line[1][0]
    return text

    # except Exception as e:
    #     print(f"Error occurred: {e}")
    #     return None
