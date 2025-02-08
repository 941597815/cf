from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

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

        # 执行 OCR 识别
        result = ocr.ocr(image, cls=False)

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
