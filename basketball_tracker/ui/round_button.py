# round_button.py

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QPushButton


class RoundButton(QPushButton):
    def __init__(self, color, hover_color, pressed_color, text, parent=None):
        super().__init__(parent)
        self.default_color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text = text
        self.init_ui()

    def init_ui(self):
        self.setText(self.text)
        self.setFixedSize(QSize(200, 200))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(self.get_style(self.default_color, self.hover_color))
        self.pressed.connect(self.on_pressed)
        self.released.connect(self.on_released)

    def get_style(self, color, hover_color):
        return f"""
        QPushButton {{
            background-color: {color};
            border-radius: 100px;
            font-size: 24px;
            font-weight: bold;
            color: white;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {self.pressed_color};
        }}
        """

    def on_pressed(self):
        self.setStyleSheet(self.get_style(self.pressed_color, self.hover_color))

    def on_released(self):
        self.setStyleSheet(self.get_style(self.default_color, self.hover_color))