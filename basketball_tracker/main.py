import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from ui.main_window import MainWindow

from core.signal_distributor import SignalDistributor as Sd
from core.state_manager import StateManager as Sm
from ui.debug_log_display import DebugLogDisplay

# GLOBAL_VARIABLES from 'config.ini'
DEBUG_MODE_STATE = False
ROSTER_CSV_PATH = ""
EVENTS_CSV_PATH = ""
LOGS_FOLDER_PATH = ""
VIDEO_BROWSER_PATH = ""

def load_config():
    global DEBUG_MODE_STATE, ROSTER_CSV_PATH, EVENTS_CSV_PATH, LOGS_FOLDER_PATH, VIDEO_BROWSER_PATH
    settings = QSettings('config.ini', QSettings.Format.IniFormat)

    DEBUG_MODE_STATE = settings.value('States/DEBUG_MODE_STATE', 'false').lower() == 'true'
    ROSTER_CSV_PATH = settings.value('Paths/ROSTER_CSV_PATH', "")
    EVENTS_CSV_PATH = settings.value('Paths/EVENTS_CSV_PATH', "")
    LOGS_FOLDER_PATH = settings.value('Paths/LOGS_FOLDER_PATH', "")
    VIDEO_BROWSER_PATH = settings.value('Paths/VIDEO_BROWSER_PATH', "")

def main():
    load_config()
    app = QApplication(sys.argv)

    print(f"Debug Mode State: {DEBUG_MODE_STATE}")
    print(f"Roster CSV Path: {ROSTER_CSV_PATH}")
    print(f"Events CSV Path: {EVENTS_CSV_PATH}")
    print(f"Logs Folder Path: {LOGS_FOLDER_PATH}")
    print(f"Video Browse Path: {VIDEO_BROWSER_PATH}")

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
