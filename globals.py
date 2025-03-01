# 定义全局变量
class Globals:
    class cf:
        guaji = False
        zhunbei=False

    def __init__(self):
        self.running = False
        self.firebtn = "p" 
        self.jtl = True
        self.jujiqiang = False
        self.buqiang = True
        self.mouseLeft = False
        self.auto_fire = False
        self.fireDelay = 30 #开火延迟ms
        self.similarity = 0.87 #红名相似度
# 创建全局变量实例
globals_instance = Globals()