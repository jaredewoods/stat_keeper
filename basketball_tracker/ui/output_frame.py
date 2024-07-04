# output_frame.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class OutputFrame(QWidget):
    def __init__(self, parent=None, theme_manager=None):
        super().__init__(parent)
        self.theme_manager = theme_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.label = QLabel("Output Frame", self)
        layout.addWidget(self.label)

    def update_content(self, content):
        self.label.setText(content)
