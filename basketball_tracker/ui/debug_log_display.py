# debug_log_display.py

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class DebugLogDisplay(QWidget):
    def __init__(self, signal_distributor, state_manager):
        super().__init__()
        self.sd = signal_distributor
        self.sm = state_manager

        self.setWindowTitle("Debug Log Display")
        self.resize(600, 400)

        self.layout = QVBoxLayout()
        self.debug_display = QTextEdit()
        self.debug_display.setReadOnly(True)
        self.debug_display.append("DebugLogDisplay Initialized.\n")
        print("3 DebugLogDisplay Initialized")

        self.layout.addWidget(self.debug_display)
        self.setLayout(self.layout)

    @pyqtSlot(str)
    def append_debug_message(self, message):
        self.debug_display.append(message)


