import time
import math

import random as rnd  # 使用别名避免冲突

def generate_normal_random(mean, stddev):
    # 生成两个均匀分布的随机数（0到1之间）
    u1 = rnd.uniform(0, 1)
    u2 = rnd.uniform(0, 1)
    # 使用Box-Muller变换转换成正态分布随机数
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    # 使用均值和标准差进行线性变换，并四舍五入
    return round(mean + z0 * stddev)

def my_random(m, n):  # 修改函数名，避免与标准库冲突
    mean = (m + n) / 2
    # 使用1.645作为基准，因为1.645分位对应单侧95%概率
    sigma = (n - m) / (2 * 1.645)
    generated_random = generate_normal_random(mean, sigma)
    # 确保生成的随机数不小于m
    if generated_random < m:
        # 如果生成的随机数小于m，补一个均匀分布的随机数
        generated_random = rnd.randint(m, n)
    # 打印调试信息（仅当m=10时）
    # if m == 10:
        # print(f"{generated_random}\n")
    return generated_random

# 示例用法
# print(my_random(11, 22))  # 输出一个在11到22之间的正态分布随机数
def random_delay_ms(min_ms, max_ms):
    
    time.sleep(my_random(min_ms,max_ms)/1000)  # 将毫秒转换为秒并延时
    # print(f"延时了 {delay_ms} 毫秒")

# 测试延时
# print(random(11, 22))
