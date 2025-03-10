import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from qfluentwidgets import SwitchButton, Slider, ComboBox, DoubleSpinBox, setTheme, Theme

# from globals import globals_instance  # 导入你定义的全局变量实例

class SettingsWindow(QWidget):
    def __init__(self, globals_instance):
        super().__init__()
        self.setWindowTitle("全局变量设置")
        self.resize(600, 400)
        setTheme(Theme.LIGHT)  # 设置主题为浅色模式
        # globals_instance = globals_instance

        # 创建主布局
        self.main_layout = QVBoxLayout(self)

        # 创建控件并添加到布局
        self.create_widgets(globals_instance)

    def create_widgets(self,globals_instance):
        # running: 开关按钮
        self.running_label = QLabel("运行状态 (running):")
        self.running_switch = SwitchButton()
        self.running_switch.setChecked(globals_instance.running)
        self.running_switch.checkedChanged.connect(lambda key: self.on_running_toggled(key, globals_instance))
        self.main_layout.addWidget(self.running_label)
        self.main_layout.addWidget(self.running_switch)

        # shandun: 开关按钮
        self.shandun_label = QLabel("闪盾 (shandun):")
        self.shandun_switch = SwitchButton()
        self.shandun_switch.setChecked(globals_instance.shandun)
        self.main_layout.addWidget(self.shandun_label)
        self.main_layout.addWidget(self.shandun_switch)

        # liantiao: 开关按钮
        self.liantiao_label = QLabel("连调 (liantiao):")
        self.liantiao_switch = SwitchButton()
        self.liantiao_switch.setChecked(globals_instance.liantiao)
        self.liantiao_switch.checkedChanged.connect(lambda key: self.on_liantiao_toggled(key, globals_instance))
        self.main_layout.addWidget(self.liantiao_label)
        self.main_layout.addWidget(self.liantiao_switch)

        # firebtn: 下拉选择框
        self.firebtn_label = QLabel("开火按钮 (firebtn):")
        self.firebtn_combo = ComboBox()
        self.firebtn_combo.addItems(["p", "a", "b", "c"])  # 假设支持的按钮
        self.firebtn_combo.setCurrentText(globals_instance.firebtn)
        self.firebtn_combo.currentTextChanged.connect(lambda key: self.on_firebtn_changed(key, globals_instance))
        self.main_layout.addWidget(self.firebtn_label)
        self.main_layout.addWidget(self.firebtn_combo)

        # jtl: 开关按钮
        self.jtl_label = QLabel("斤斗浪 (jtl):")
        self.jtl_switch = SwitchButton()
        self.jtl_switch.setChecked(globals_instance.jtl)
        self.jtl_switch.checkedChanged.connect(lambda key: self.on_jtl_toggled(key, globals_instance))
        self.main_layout.addWidget(self.jtl_label)
        self.main_layout.addWidget(self.jtl_switch)

        # jujiqiang: 开关按钮
        self.jujiqiang_label = QLabel("聚聚枪 (jujiqiang):")
        self.jujiqiang_switch = SwitchButton()
        self.jujiqiang_switch.setChecked(globals_instance.jujiqiang)
        self.jujiqiang_switch.checkedChanged.connect(lambda key: self.on_jujiqiang_toggled(key, globals_instance))
        self.main_layout.addWidget(self.jujiqiang_label)
        self.main_layout.addWidget(self.jujiqiang_switch)

        # buqiang: 开关按钮
        self.buqiang_label = QLabel("不抢 (buqiang):")
        self.buqiang_switch = SwitchButton()
        self.buqiang_switch.setChecked(globals_instance.buqiang)
        self.buqiang_switch.checkedChanged.connect(lambda key: self.on_buqiang_toggled(key, globals_instance))
        self.main_layout.addWidget(self.buqiang_label)
        self.main_layout.addWidget(self.buqiang_switch)

        # mouseLeft: 开关按钮
        self.mouseLeft_label = QLabel("鼠标左键 (mouseLeft):")
        self.mouseLeft_switch = SwitchButton()
        self.mouseLeft_switch.setChecked(globals_instance.mouseLeft)
        self.mouseLeft_switch.checkedChanged.connect(lambda key: self.on_mouseLeft_toggled(key, globals_instance))
        self.main_layout.addWidget(self.mouseLeft_label)
        self.main_layout.addWidget(self.mouseLeft_switch)

        # auto_fire: 开关按钮
        self.auto_fire_label = QLabel("自动开火 (auto_fire):")
        self.auto_fire_switch = SwitchButton()
        self.auto_fire_switch.setChecked(globals_instance.auto_fire)
        self.auto_fire_switch.checkedChanged.connect(lambda key: self.on_auto_fire_toggled(key, globals_instance))
        self.main_layout.addWidget(self.auto_fire_label)
        self.main_layout.addWidget(self.auto_fire_switch)

        # fireDelay: 滑动条
        self.fireDelay_label = QLabel(f"开火延迟 (fireDelay): {globals_instance.fireDelay} ms")
        self.fireDelay_slider = Slider()
        self.fireDelay_slider.setMinimum(10)
        self.fireDelay_slider.setMaximum(100)
        self.fireDelay_slider.setValue(globals_instance.fireDelay)
        self.fireDelay_slider.valueChanged.connect(lambda key: self.on_fireDelay_changed(key, globals_instance))
        self.main_layout.addWidget(self.fireDelay_label)
        self.main_layout.addWidget(self.fireDelay_slider)

        # similarity: 数值输入框
        self.similarity_label = QLabel(f"红名相似度 (similarity): {globals_instance.similarity}")
        self.similarity_spin = DoubleSpinBox()
        self.similarity_spin.setRange(0.5, 1.0)
        self.similarity_spin.setSingleStep(0.01)
        self.similarity_spin.setValue(globals_instance.similarity)
        self.similarity_spin.valueChanged.connect(lambda key: self.on_similarity_changed(key, globals_instance))
        self.main_layout.addWidget(self.similarity_label)
        self.main_layout.addWidget(self.similarity_spin)

    # 定义回调函数，用于更新全局变量
    def on_running_toggled(self, checked,globals_instance):
        globals_instance.running = checked

    def on_shandun_toggled(self, checked,globals_instance):
        globals_instance.shandun = checked

    def on_liantiao_toggled(self, checked,globals_instance):
        globals_instance.liantiao = checked

    def on_firebtn_changed(self, text,globals_instance):
        globals_instance.firebtn = text

    def on_jtl_toggled(self, checked,globals_instance):
        globals_instance.jtl = checked

    def on_jujiqiang_toggled(self, checked,globals_instance):
        globals_instance.jujiqiang = checked

    def on_buqiang_toggled(self, checked,globals_instance):
        globals_instance.buqiang = checked

    def on_mouseLeft_toggled(self, checked,globals_instance):
        globals_instance.mouseLeft = checked

    def on_auto_fire_toggled(self, checked,globals_instance):
        globals_instance.auto_fire = checked

    def on_fireDelay_changed(self, value,globals_instance):
        globals_instance.fireDelay = value
        self.fireDelay_label.setText(f"开火延迟 (fireDelay): {value} ms")

    def on_similarity_changed(self, value,globals_instance):
        globals_instance.similarity = value
        self.similarity_label.setText(f"红名相似度 (similarity): {value}")

def start_ui(globals_instance):
    app = QApplication(sys.argv)
    window = SettingsWindow(globals_instance)
    window.show()
    sys.exit(app.exec())

# if __name__ == "__main__":
#     start_ui(globals_instance)