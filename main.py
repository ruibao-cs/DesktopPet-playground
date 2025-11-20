import sys, random
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QPainter, QColor, QPixmap, QTransform
import objc
from AppKit import NSApp, NSWindow, NSWindowCollectionBehaviorCanJoinAllSpaces
from Quartz import kCGDesktopWindowLevelKey, CGWindowLevelForKey



class DesktopPet(QLabel):
    def __init__(self):
        super().__init__()

        # 无边框 + 置顶 + 透明背景
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)


        def load_and_scale(path):
            return QPixmap(path).scaled(
                100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

        # 载入多个图片
        # 单个载入照片格式：self.frames = QPixmap("assets/sit_1.png"),]
        self.animations = {
            "idle": [
                load_and_scale("assets/idle_1.png"),
                load_and_scale("assets/idle_2.png"),
                load_and_scale("assets/idle_3.png"),
                load_and_scale("assets/idle_2(2).png"),
            ],
            "walk": [
                load_and_scale("assets/walk_0.png"),
                load_and_scale("assets/walk_1.png"),
                load_and_scale("assets/walk_2.png"),
            ],
        }


        # 当前状态 & 帧索引
        self.current_state = "idle"
        self.current_frame_index = 0
        self.current_pixmap = self.animations[self.current_state][self.current_frame_index]
        self.facing_right = True

        self.resize(self.current_pixmap.size())

        # 移动速度（向右为正，向左为负）
        self.vx = 0

        # 定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(360)

        # 随机行为用的计时器：每隔一段时间随机决定“走 or 坐”
        self.behavior_timer = QTimer(self)
        self.behavior_timer.timeout.connect(self.random_behavior)
        self.behavior_timer.start(5000)

        # 放到屏幕中间
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # 鼠标拖动用到的变量
        self.mouse_over= False
        self.dragging = False
        self.drag_offset = QPoint()

        # self.setDesktopLevel()
        self.show()
        self.disableShadow()
        


    def disableShadow(self):
        """
        最小改动版本：只关掉 macOS 窗口阴影，不改层级、不改桌面。
        """
        try:
            from AppKit import NSApp
        except ImportError:
            return  # 没装 PyObjC 就直接跳过

        qt_window = self.window().windowHandle()
        if qt_window is None:
            return

        app = NSApp()
        windows = list(app.windows())
        if not windows:
            return

        # 简单粗暴：拿最后一个 NSWindow，当成我们的宠物窗口
        nswin = windows[-1]

        try:
            nswin.setHasShadow_(False)
        except Exception:
            pass


    def next_frame(self):
        """
        切换到下一帧。这里也做移动逻辑（如果 current_state == 'walk' 且未被鼠标覆盖）。
        """
        # 移动逻辑（尽量不改现有函数签名）
        if self.current_state == "walk" and not self.mouse_over and not self.dragging:
            # 如果 vx 为 0，保证至少有速度（fallback）
            if self.vx == 0:
                self.vx = 4 if self.facing_right else -4

            x = self.x() + self.vx
            screen = QApplication.primaryScreen().geometry()

            # 碰到左右边界时反向并修正位置
            if x < 0:
                x = 0
                self.vx = abs(self.vx)
                self.facing_right = True
            elif x + self.width() > screen.width():
                x = screen.width() - self.width()
                self.vx = -abs(self.vx)
                self.facing_right = False

            # 保持垂直位置不变（你可以按需调整 y）
            self.move(x, self.y())

        # 帧切换逻辑（保持原有行为）
        frames = self.animations[self.current_state]
        # 如果只有一帧（比如 idle），保持不变；多帧就循环
        if self.current_frame_index < 0:
            self.current_frame_index = 0
        elif len(frames) > 1:
            self.current_frame_index = (self.current_frame_index + 1) % len(frames)
        else:
            self.current_frame_index = 0

        base_pix = frames[self.current_frame_index]

        # 镜像处理：向左画时水平翻转
        if self.facing_right:
            t = QTransform()
            t.scale(-1, 1)
            flipped = base_pix.transformed(t)
            self.current_pixmap = flipped
        else:
            self.current_pixmap = base_pix

        self.update() 

    def switch_state(self, new_state):
        """切换状态时调用，比如从 idle 切到 walk"""
        if new_state == self.current_state:
            return
        if new_state not in self.animations:
            return
        self.current_state = new_state
        self.current_frame_index = -1
        # self.current_pixmap = self.animations[self.current_state][0]
        self.update()

    def paintEvent(self, event):
        """
        显示图片。
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # painter.drawPixmap(0, 0, self.pixmap)
        painter.drawPixmap(0, 0, self.current_pixmap)

    # 以下是拖动相关
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_offset = event.globalPosition().toPoint() - self.pos()
            event.accept()
        elif event.button() == Qt.RightButton:
            # QApplication.quit()
            if self.current_state == "idle":
                self.switch_state("walk")
            else:
                self.switch_state("idle")

    def mouseMoveEvent(self, event):
        if self.dragging and event.buttons() & Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_offset
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()
    
    def enterEvent(self, event):
        # 鼠标覆盖：标记为覆盖（不移动）并在 walk 时保持第一帧
        self.mouse_over = True
        # 如果在 walk 状态想显示固定帧（你提到的要求），强制frame=0
        if self.current_state == "walk":
            self.current_frame_index = 0
            # self.current_pixmap = self.animations["walk"][0]
            self.update()

    def leaveEvent(self, event):
        self.mouse_over = False

    # 随机切换移动状态
    def random_behavior(self):
        # 如果在拖动或鼠标覆盖时不要打断
        if self.dragging or self.mouse_over:
            return

        # 随机选择 idle 或 walk（权重可调整）
        choice = random.choices(["idle", "walk"], weights=[0.6, 0.4])[0]
        if choice == "idle":
            self.switch_state("idle")
            self.vx = 0
        else:
            # 切走路并随机方向
            self.switch_state("walk")
            self.facing_right = random.choice([True, False])
            self.vx = 4 if self.facing_right else -4

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    pet.show()
    sys.exit(app.exec())
