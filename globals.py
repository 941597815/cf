# 定义全局变量
class Globals:
    class cf:
        guaji = False
        zhunbei = False

    def __init__(self):
        self.debug = False
        self.osd = True
        self.game_status = False
        self.running = False
        self.shandun = False
        self.liantiao = False
        self.firebtn = "p"  # 开火按键 a-z,0-9
        self.jtl = False
        self.jujiqiang = False
        self.buqiang = True  # 默认步枪模式
        self.usp = False
        self.mouseLeft = False
        self.weapons_identification = False  # F5 武器自动识别，开启后可能会引起卡顿
        self.auto_fire = False  # F7 红名自动开火
        self.fireDelay = 30  # 开火延迟ms
        self.similarity = 0.87  # 红名相似度
        self.resolution = 2  # 游戏分辨率：1=1600x900 2=1920x1080 3=2560x1440


# 创建全局变量实例
globals_instance = Globals()
