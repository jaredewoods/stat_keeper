import sys
from PyQt6.QtCore import QSettings, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar
from PyQt6.QtGui import QAction

from core.signal_distributor import SignalDistributor
from core.state_manager import StateManager
from data.rosters_dao import RostersDAO
from data.events_dao import EventsDAO
from data.player_stats_dao import PlayerStatsDAO
from ui.floating_control import FloatingControl
from video.video_window import VideoWindow
from video.video_control_window import VideoControlWindow
from video.transport_control import TransportControl
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
        self.rosters_dao = RostersDAO()
        self.events_dao = EventsDAO()
        self.player_stats_dao = PlayerStatsDAO()

        self.load_configurations()
        self.main_window = MainWindow(self.sd, self.sm)
        self.main_window.move(0, 0)
        self.main_window.show()

        self.video_window = VideoWindow()
        self.video_window.move(0, 0)
        self.video_window.hide()

        self.floating_control = FloatingControl(self.sd, self.sm)
        self.floating_control.move(0, 0)
        self.floating_control.hide()

        self.video_control_window = VideoControlWindow(self.video_window, self.sd, self.sm)
        self.video_control_window.move(0, 570)
        self.video_control_window.hide()

        self.transport_control = TransportControl(self.sd, self.sm)
        self.transport_control.hide()

        self.setup_menu()
        self.connect_signals_to_slots()
        sys.exit(self.app.exec())

    def setup_menu(self):
        # Set up the menu bar and menus
        menu_bar = QMenuBar(self.main_window)

        # File Menu
        file_menu = menu_bar.addMenu("File")

        # Open Action
        open_action = QAction("Open", self.main_window)
        open_action.triggered.connect(self.video_control_window.open_file)  # Connect to open_file method
        file_menu.addAction(open_action)

        quit_action = QAction("Quit", self.main_window)
        quit_action.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(quit_action)

        # Window Menu
        window_menu = menu_bar.addMenu("Window")

        self.video_window_action = QAction("Video Window", self.main_window, checkable=True)
        self.video_window_action.triggered.connect(self.toggle_video_window)
        window_menu.addAction(self.video_window_action)

        self.floating_control_action = QAction("Floating Control", self.main_window, checkable=True)
        self.floating_control_action.triggered.connect(self.toggle_floating_control)
        window_menu.addAction(self.floating_control_action)

        self.video_control_window_action = QAction("Video Control Window", self.main_window, checkable=True)
        self.video_control_window_action.triggered.connect(self.toggle_video_control_window)
        window_menu.addAction(self.video_control_window_action)

        self.transport_control_action = QAction("Transport Control", self.main_window, checkable=True)
        self.transport_control_action.triggered.connect(self.toggle_transport_control)
        window_menu.addAction(self.transport_control_action)

        # Adding Control, Input, and Output Frames to Window Menu
        self.control_frame_action = QAction("Control Frame", self.main_window, checkable=True)
        self.control_frame_action.setChecked(True)
        self.control_frame_action.triggered.connect(self.toggle_control_frame)
        window_menu.addAction(self.control_frame_action)

        self.input_frame_action = QAction("Input Frame", self.main_window, checkable=True)
        self.input_frame_action.setChecked(True)
        self.input_frame_action.triggered.connect(self.toggle_input_frame)
        window_menu.addAction(self.input_frame_action)

        self.output_frame_action = QAction("Output Frame", self.main_window, checkable=True)
        self.output_frame_action.setChecked(True)
        self.output_frame_action.triggered.connect(self.toggle_output_frame)
        window_menu.addAction(self.output_frame_action)

        # Edit Menu
        edit_menu = menu_bar.addMenu("Edit")

        edit_database_action = QAction("Edit Database", self.main_window)
        edit_menu.addAction(edit_database_action)  # Placeholder, no connection yet
        edit_logs_action = QAction("Edit Roster", self.main_window)
        edit_menu.addAction(edit_logs_action)  # Placeholder, no connection yet
        edit_logs_action = QAction("Edit Events", self.main_window)
        edit_menu.addAction(edit_logs_action)  # Placeholder, no connection yet

        self.main_window.setMenuBar(menu_bar)

    def toggle_video_window(self):
        if self.video_window_action.isChecked():
            self.video_window.show()
        else:
            self.video_window.hide()

    def toggle_floating_control(self):
        if self.floating_control_action.isChecked():
            self.floating_control.show()
        else:
            self.floating_control.hide()

    def toggle_video_control_window(self):
        if self.video_control_window_action.isChecked():
            self.video_control_window.show()
        else:
            self.video_control_window.hide()

    def toggle_transport_control(self):
        if self.transport_control_action.isChecked():
            self.transport_control.show()
        else:
            self.transport_control.hide()

    def toggle_control_frame(self):
        if self.control_frame_action.isChecked():
            self.main_window.control_frame.show()
        else:
            self.main_window.control_frame.hide()

    def toggle_input_frame(self):
        if self.input_frame_action.isChecked():
            self.main_window.input_frame.show()
        else:
            self.main_window.input_frame.hide()

    def toggle_output_frame(self):
        if self.output_frame_action.isChecked():
            self.main_window.output_frame.show()
        else:
            self.main_window.output_frame.hide()

    def emit_test_debug_signals(self):
        self.sd.SIG_DebugMessage.emit(f"Debug Mode State: {DEBUG_MODE_STATE}")
        self.sd.SIG_DebugMessage.emit(f"Logs Folder Path: {LOGS_FOLDER_PATH}")
        self.sd.SIG_DebugMessage.emit(f"Video Browse Path: {VIDEO_BROWSER_PATH}")

    @staticmethod
    def load_configurations():
        global DEBUG_MODE_STATE, LOGS_FOLDER_PATH, VIDEO_BROWSER_PATH
        _settings = QSettings('config.ini', QSettings.Format.IniFormat)
        # The second argument, either false or "" are the fallback settings if the ini file is invalid
        DEBUG_MODE_STATE = _settings.value('States/DEBUG_MODE_STATE', 'false').lower() == 'true'
        LOGS_FOLDER_PATH = _settings.value('Paths/LOGS_FOLDER_PATH', "")
        VIDEO_BROWSER_PATH = _settings.value('Paths/VIDEO_BROWSER_PATH', "")

    def connect_signals_to_slots(self):
        self.sd.SIG_DebugMessage.connect(self.main_window.output_frame.append_debug_message)
        self.sd.SIG_ClearAllTables.connect(self.player_stats_dao.clear_all_tables)
        self.sd.SIG_FieldDataRetrieved.connect(self.player_stats_dao.update_player_stats)
        self.sd.SIG_FieldDataRetrieved.connect(self.main_window.output_frame.append_event_log)
        self.sd.SIG_FieldDataRetrieved.connect(self.main_window.output_frame.refresh_database_tab)
        self.sd.SIG_FieldDataRetrieved.connect(self.main_window.output_frame.refresh_stats_tab)
        self.sd.SIG_EventCodeSelected.connect(self.main_window.input_frame.event_code_selected)
        self.sd.SIG_RosterPlayerSelected.connect(self.main_window.input_frame.player_selected)
        self.sd.SIG_BackToZeroButtonClicked.connect(self.video_control_window.back_to_zero)
        self.sd.SIG_Back20ButtonClicked.connect(self.video_control_window.back20)
        self.sd.SIG_Back10ButtonClicked.connect(self.video_control_window.back10)
        self.sd.SIG_ChangePlaybackSpeedButtonClicked.connect(self.video_control_window.change_playback_speed)
        self.sd.SIG_PauseButtonClicked.connect(self.video_control_window.pause_video)
        self.sd.SIG_CaptureButtonClicked.connect(self.main_window.control_frame.capture_timecode)
        self.sd.SIG_CaptureButtonClicked.connect(self.main_window.input_frame.show_event_entry_tab)
        self.sd.SIG_UndoButtonClicked.connect(self.player_stats_dao.delete_last_added_row)
        self.sd.SIG_UndoButtonClicked.connect(self.main_window.output_frame.refresh_database_tab)
        self.sd.SIG_PlayButtonClicked.connect(self.video_control_window.play_video)
        self.sd.SIG_LogEntriesButtonClicked.connect(self.main_window.input_frame.log_entries)
        self.sd.SIG_ShowVideoWindow.connect(self.video_window.show)
        self.sd.SIG_TimeUpdate.connect(self.main_window.control_frame.update_time)
        self.sd.SIG_EnterCapturedTimecode.connect(self.main_window.input_frame.enter_captured_timecode)
        print("4 Signals and Slots connected")

if __name__ == "__main__":
    Main()
