import sys

from PyQt6.QtCore import QSettings, QObject
from PyQt6.QtWidgets import QApplication

from core.signal_distributor import SignalDistributor
from core.state_manager import StateManager
from ui.debug_log_display import DebugLogDisplay
from ui.floating_controls import FloatingControls
from video.video_window import VideoWindow
from video.video_control_window import VideoControlWindow
from ui.main_window import MainWindow

# GLOBAL_VARIABLES from 'config.ini'
DEBUG_MODE_STATE = False
LOGS_FOLDER_PATH = ""
VIDEO_BROWSER_PATH = ""

class Main(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.sd = SignalDistributor()
        self.sm = StateManager(self.sd)

        self.load_configurations()

        self.debug_log_display = DebugLogDisplay(self.sd, self.sm)
        self.main_window = MainWindow(self.sd, self.sm)
        self.main_window.move(840, 0)
        self.main_window.show()

        self.video_window = VideoWindow()
        self.video_window.move(0, 440)
        self.video_window.show()
        self.floating_controls = FloatingControls(self.sd, self.sm)
        self.floating_controls.move(600, 0)
        self.floating_controls.show()
        self.video_control_window = VideoControlWindow(self.video_window)
        self.video_control_window.move(800, 640)
        self.video_control_window.show()

        self.connect_signals_to_slots()

        if DEBUG_MODE_STATE:
            self.debug_log_display.show()
            self.debug_log_display.move(0, 0)
        self.emit_test_debug_signals()

        sys.exit(self.app.exec())

    def emit_test_debug_signals(self):
        self.sd.SIG_DebugMessage.emit(f"Debug Mode State: {DEBUG_MODE_STATE}")
        self.sd.SIG_DebugMessage.emit(f"Logs Folder Path: {LOGS_FOLDER_PATH}")
        self.sd.SIG_DebugMessage.emit(f"Video Browse Path: {VIDEO_BROWSER_PATH}")

    @staticmethod
    def load_configurations():
        global DEBUG_MODE_STATE, LOGS_FOLDER_PATH, VIDEO_BROWSER_PATH
        _settings = QSettings('config.ini', QSettings.Format.IniFormat)
        DEBUG_MODE_STATE = _settings.value('States/DEBUG_MODE_STATE', 'false').lower() == 'true'
        LOGS_FOLDER_PATH = _settings.value('Paths/LOGS_FOLDER_PATH', "")
        VIDEO_BROWSER_PATH = _settings.value('Paths/VIDEO_BROWSER_PATH', "")

    def connect_signals_to_slots(self):
        self.sd.SIG_DebugMessage.connect(self.debug_log_display.append_debug_message)
        print("6 Signals and Slots connected")

if __name__ == "__main__":
    Main()
