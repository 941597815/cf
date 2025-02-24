import random
import time
import math
import pyautogui
from pyautogui import easeOutQuad, easeInOutQuad

def calculate_distance(start, end):
    """计算两点间距离"""
    return math.hypot(end[0]-start[0], end[1]-start[1])

def human_curve_v2(start, end, distortion=0.6):
    """优化版自适应贝塞尔曲线生成"""
    # 根据距离动态控制点数
    distance = calculate_distance(start, end)
    points_num = min(max(int(distance * 0.6), 80), 300)  # 动态点数
    
    # 生成控制点（使用三次贝塞尔曲线）
    ctrl_pts = [start]
    offset_range = distance * 0.3 * distortion  # 动态偏移范围
    
    # 生成两个中间控制点
    for _ in range(2):
        ctrl_x = start[0] + (end[0] - start[0]) * random.uniform(0.2, 0.8)
        ctrl_y = start[1] + (end[1] - start[1]) * random.uniform(0.2, 0.8)
        ctrl_x += random.uniform(-offset_range, offset_range)
        ctrl_y += random.uniform(-offset_range, offset_range)
        ctrl_pts.append((int(ctrl_x), int(ctrl_y)))
    ctrl_pts.append(end)

    # 三次贝塞尔曲线计算
    curve = []
    for t in (i / points_num for i in range(points_num + 1)):
        x = (1 - t)**3 * ctrl_pts[0][0] + 3*(1 - t)**2*t * ctrl_pts[1][0] + 3*(1 - t)*t**2 * ctrl_pts[2][0] + t**3 * ctrl_pts[3][0]
        y = (1 - t)**3 * ctrl_pts[0][1] + 3*(1 - t)**2*t * ctrl_pts[1][1] + 3*(1 - t)*t**2 * ctrl_pts[2][1] + t**3 * ctrl_pts[3][1]
        curve.append((x, y))
    
    return curve

def smooth_ease(t):
    """复合缓动函数"""
    return 0.5 * (easeInOutQuad(t) + 0.5 * (1 - math.cos(t * math.pi)) / 2)

def optimized_human_move(end_pos, duration=1.5, distortion=0.5):
    """优化版拟人移动"""
    start_pos = pyautogui.position()
    
    # 生成高精度路径
    path = human_curve_v2(start_pos, end_pos, distortion)
    
    # 添加平滑抖动
    path = [
        (
            x + 0.8 * math.sin(i * 0.3) + random.uniform(-0.5, 0.5),
            y + 0.8 * math.cos(i * 0.35) + random.uniform(-0.5, 0.5)
        )
        for i, (x, y) in enumerate(path)
    ]
    
    # 生成时间序列（复合缓动）
    total_points = len(path)
    timestamps = [smooth_ease(i / total_points) for i in range(total_points)]
    
    # 计算间隔时间（保持最小时间间隔）
    base_duration = duration / total_points
    durations = []
    for i in range(len(path)-1):
        delta = timestamps[i+1] - timestamps[i]
        durations.append(max(
            base_duration * delta * random.uniform(0.9, 1.1),  # 添加时间扰动
            0.0015  # 最小时间间隔
        ))
    
    # 高频移动执行
    start_time = time.time()
    for i in range(1, len(path)):
        elapsed = time.time() - start_time
        if elapsed > duration * 1.2:  # 超时保护
            break
            
        # 使用相对移动提高精度
        dx = path[i][0] - path[i-1][0]
        dy = path[i][1] - path[i-1][1]
        pyautogui.moveRel(dx, dy, duration=durations[i-1], _pause=False)
        
        # 精确时间控制
        time.sleep(durations[i-1] * 0.8)  # 补偿系统延迟
    
    # 最终定位
    pyautogui.moveTo(end_pos[0], end_pos[1], duration=0.08)

# 使用示例
if __name__ == "__main__":
    screen_width, screen_height = pyautogui.size()
    target = (screen_width//2, screen_height//2)
    
    optimized_human_move(target, duration=5.8, distortion=0.6)