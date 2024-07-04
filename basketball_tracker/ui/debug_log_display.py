# debug_log_display.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtCore import pyqtSlot

class DebugLogDisplay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the UI
        self.setWindowTitle("Debug Log Display")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.debug_display = QTextEdit()
        self.debug_display.setReadOnly(True)

        self.layout.addWidget(self.debug_display)
        self.setLayout(self.layout)

    @pyqtSlot(str)
    def append_debug_message(self, message: str):

        """
        Slot to handle incoming log messages.
        """
        self.debug_display.append(message)