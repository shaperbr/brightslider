import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel, QDesktopWidget, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class OSDSlider(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(9)
        self.slider.setTickPosition(QSlider.TicksLeft)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.set_screenpad_brightness)
        layout.addWidget(self.slider)

        self.setLayout(layout)

        # Estilo personalizado
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 10px;
            }
            QLabel {
                color: white;
            }
            QSlider::groove:vertical {
                background-color: rgba(255, 255, 255, 100);
                width: 6px;
                border-radius: 3px;
            }
            QSlider::handle:vertical {
                background-color: white;
                border: none;
                height: 20px;
                width: 20px;
                margin: 0 -7px;
                border-radius: 10px;
            }
            QSlider::add-page:vertical {
                background-color: rgba(0, 0, 0, 100);
            }
            QSlider::sub-page:vertical {
                background-color: rgba(0, 0, 0, 100);
            }
            QSlider::tick:vertical {
                background-color: white;
                width: 1px;
                height: 6px;
            }
        """)

    def set_screenpad_brightness(self, value):
        self.label.setText(f"{value}")
        if value == 0:
            subprocess.run(["screenpad", "off"])
        else:
            subprocess.run(["screenpad", str(value)])

    def move_to_target_screen(self):
        desktop = QApplication.desktop()
        target_screen = None
        target_screen_geometry = None

        for i in range(desktop.screenCount()):
            screen_geometry = desktop.screenGeometry(i)
            if screen_geometry.width() == 1920 and screen_geometry.height() == 515:
                target_screen = i
                target_screen_geometry = screen_geometry
                break

        if target_screen is not None:
            self.move(target_screen_geometry.left(), target_screen_geometry.top())
        else:
            print("Tela com resolução 1920x515 não encontrada.")

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, osd_slider, parent=None):
        super(SystemTrayIcon, self).__init__(parent)
        self.setIcon(QIcon("/opt/brightslider/icon.svg"))  # Substitua "icon.png" pelo caminho para o ícone desejado

        self.osd_slider = osd_slider

        # Criando menu de contexto
        self.menu = QMenu(parent)

        self.show_action = QAction("Show OSD", self.menu)
        self.show_action.triggered.connect(self.show_osd_slider)
        self.menu.addAction(self.show_action)

        self.hide_action = QAction("Hide OSD", self.menu)
        self.hide_action.triggered.connect(self.hide_osd_slider)
        self.menu.addAction(self.hide_action)

        self.quit_action = QAction("Exit", self.menu)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)

    def show_osd_slider(self):
        self.osd_slider.show()

    def hide_osd_slider(self):
        self.osd_slider.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    osd_slider = OSDSlider()
    osd_slider.move_to_target_screen()
    osd_slider.show()

    system_tray_icon = SystemTrayIcon(osd_slider)
    system_tray_icon.show()

    sys.exit(app.exec_())

