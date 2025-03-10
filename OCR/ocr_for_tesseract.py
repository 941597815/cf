import cv2
import numpy as np
import pytesseract
from PIL import Image

# 如果是 Windows 系统，需要指定 Tesseract 的路径
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image_path):
    """加载图像并进行预处理"""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 转为灰度图像
    _, binary_img = cv2.threshold(
        img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )  # 二值化处理
    kernel = np.ones((2, 2), np.uint8)
    processed_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)  # 形态学去噪
    return processed_img


def extract_text(image_path):
    """使用 Tesseract OCR 提取图像中的文本"""
    processed_img = preprocess_image(image_path)
    pil_img = Image.fromarray(processed_img)
    custom_config = r"--oem 3 --psm 6"  # 设置 Tesseract 参数
    text = pytesseract.image_to_string(pil_img, config=custom_config)
    return text.strip()


if __name__ == "__main__":
    image_path = "./image.png"  # 替换为你的图像路径
    result_text = extract_text(image_path)
    print("识别结果：")
    print(result_text)
    print(bool(""))
