import cv2
import numpy as np

def has_red_text_based_on_rgb(image, target_rgb=(242, 74, 23), similarity=1.0,
                             min_area=100, edge_density_threshold=0.1):
    """
    通过 RGB 颜色和相似度检测图像中是否存在红色文字
    
    :param image: 输入图像（屏幕截图或文件路径）
    :param target_rgb: 目标 RGB 颜色，默认值为 (242, 74, 23)
    :param similarity: 0-1 的相似度，1 表示完全匹配
    :param min_area: 最小文字区域面积
    :param edge_density_threshold: 边缘密度阈值
    :return: 是否存在红色文字
    """
    # 将屏幕截图转换为 OpenCV 格式
    if isinstance(image, str):
        img = cv2.imread(image)
    else:
        img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if img is None:
        raise ValueError("Image not found or unable to load.")
    
    # 将目标 RGB 颜色转换为 HSV
    target_rgb = np.uint8([[target_rgb]])
    target_hsv = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2HSV)[0][0]
    target_hue, target_saturation, target_value = target_hsv
    
    # 动态调整 HSV 范围
    hue_range = int(180 * (1 - similarity))
    saturation_range = int(255 * (1 - similarity))
    value_range = int(255 * (1 - similarity))
    # 计算 HSV 范围，确保不溢出
    hsv_lower = np.array([
        max(0, target_hue - hue_range),
        max(0, target_saturation - saturation_range),
        max(0, target_value - value_range)
    ])

    hsv_upper = np.array([
        min(179, target_hue + hue_range),
        min(255, target_saturation + saturation_range),
        min(255, target_value + value_range)
    ])
    # # 根据相似度动态调整 HSV 范围
    # hue_range = int(180 * (1 - similarity))
    # saturation_range = int(255 * (1 - similarity))
    # value_range = int(255 * (1 - similarity))
    
    # hsv_lower = np.array([
    #     max(0, target_hue - hue_range),
    #     max(0, target_saturation - saturation_range),
    #     max(0, target_value - value_range)
    # ])
    
    # hsv_upper = np.array([
    #     min(179, target_hue + hue_range),
    #     min(255, target_saturation + saturation_range),
    #     min(255, target_value + value_range)
    # ])
    
    # 转换为 HSV 格式
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imwrite("output_1.png", hsv)
    
    # 提取目标颜色范围
    mask = cv2.inRange(hsv, hsv_lower, hsv_upper)
    cv2.imwrite("output_2.png", mask)
    
    # 形态学操作：去噪 + 连接文字区域
    kernel = np.ones((3,3), np.uint8)
    cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    dilated = cv2.dilate(cleaned, kernel, iterations=2)
    
    cv2.imwrite("output_3.png", dilated)

    # 计算边缘密度（文字区域边缘密集）
    edges = cv2.Canny(dilated, 50, 150)
    edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
    
    # 轮廓分析：筛选符合文字特征的区域
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    text_like = False
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = max(w, h) / (min(w, h) + 1e-5)
        # 条件：面积足够大 + 非极端长宽比（排除噪点/直线）
        if area > min_area and aspect_ratio < 8:
            text_like = True
            break
    
    return edge_density > edge_density_threshold or text_like
