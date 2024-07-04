import sys

from PyQt6.QtCore import QSettings, QObject
from PyQt6.QtWidgets import QApplication

from core.signal_distributor import SignalDistributor
from core.state_manager import StateManager
from ui.debug_log_display import DebugLogDisplay
from ui.floating_controls import FloatingControls
from ui.main_window import MainWindow

# GLOBAL_VARIABLES from 'config.ini'
DEBUG_MODE_STATE = False
ROSTER_CSV_PATH = ""
EVENTS_CSV_PATH = ""
LOGS_FOLDER_PATH = ""
VIDEO_BROWSER_PATH = ""

class Main(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.sd = SignalDistributor()
        self.sm = StateManager()

        self.load_configurations()

        self.debug_log_display = DebugLogDisplay(self.sd, self.sm)
        self.main_window = MainWindow(self.sd, self.sm)
        self.floating_controls = FloatingControls(self.sd, self.sm, ROSTER_CSV_PATH, EVENTS_CSV_PATH)

        self.connect_signals_to_slots()

        self.main_window.show()
        if DEBUG_MODE_STATE:
            self.debug_log_display.show()
        self.floating_controls.show()

        self.emit_test_debug_signals()

        sys.exit(self.app.exec())

    def emit_test_debug_signals(self):
        self.sd.SIG_DebugMessage.emit(f"Debug Mode State: {DEBUG_MODE_STATE}")
        self.sd.SIG_DebugMessage.emit(f"Roster CSV Path: {ROSTER_CSV_PATH}")
        self.sd.SIG_DebugMessage.emit(f"Events CSV Path: {EVENTS_CSV_PATH}")
        self.sd.SIG_DebugMessage.emit(f"Logs Folder Path: {LOGS_FOLDER_PATH}")
        self.sd.SIG_DebugMessage.emit(f"Video Browse Path: {VIDEO_BROWSER_PATH}")

    @staticmethod
    def load_configurations():
        global DEBUG_MODE_STATE, ROSTER_CSV_PATH, EVENTS_CSV_PATH, LOGS_FOLDER_PATH, VIDEO_BROWSER_PATH
        _settings = QSettings('config.ini', QSettings.Format.IniFormat)
        DEBUG_MODE_STATE = _settings.value('States/DEBUG_MODE_STATE', 'false').lower() == 'true'
        ROSTER_CSV_PATH = _settings.value('Paths/ROSTER_CSV_PATH', "")
        EVENTS_CSV_PATH = _settings.value('Paths/EVENTS_CSV_PATH', "")
        LOGS_FOLDER_PATH = _settings.value('Paths/LOGS_FOLDER_PATH', "")
        VIDEO_BROWSER_PATH = _settings.value('Paths/VIDEO_BROWSER_PATH', "")

    def connect_signals_to_slots(self):
        self.sd.SIG_DebugMessage.connect(self.debug_log_display.append_debug_message)
        print("Signals and Slots connected")

if __name__ == "__main__":
    Main()
