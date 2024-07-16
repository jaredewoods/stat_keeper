import sys

from PyQt6.QtCore import QSettings, QObject
from PyQt6.QtWidgets import QApplication

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
        self.main_window.move(300, 0)
        self.main_window.show()

        self.video_window = VideoWindow()
        self.video_window.move(0, 0)
        # self.video_window.show()

        self.floating_control = FloatingControl(self.sd, self.sm)
        self.floating_control.move(0, 0)
        self.floating_control.show()

        self.video_control_window = VideoControlWindow(self.video_window, self.sd, self.sm)
        self.video_control_window.move(0, 640)

        self.transport_control = TransportControl(self.sd, self.sm)
        self.transport_control.show()

        self.connect_signals_to_slots()
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
        self.sd.SIG_DebugMessage.connect(self.main_window.output_frame.append_debug_message)
        self.sd.SIG_EventCodeSelected.connect(self.main_window.input_frame.event_code_selected)
        self.sd.SIG_RosterPlayerSelected.connect(self.main_window.input_frame.player_selected)
        self.sd.SIG_BackToZeroButtonClicked.connect(self.video_control_window.back_to_zero)
        self.sd.SIG_Back20ButtonClicked.connect(self.video_control_window.back20)
        self.sd.SIG_Back10ButtonClicked.connect(self.video_control_window.back10)
        self.sd.SIG_ChangePlaybackSpeedButtonClicked.connect(self.video_control_window.change_playback_speed)
        self.sd.SIG_CaptureButtonClicked.connect(self.video_control_window.capture_timecode)
        self.sd.SIG_CapturePauseButtonClicked.connect(self.video_control_window.capture_pause)
        self.sd.SIG_PauseButtonClicked.connect(self.video_control_window.pause_video)
        self.sd.SIG_UndoButtonClicked.connect(self.undo)
        self.sd.SIG_PlayButtonClicked.connect(self.video_control_window.play_video)
        self.sd.SIG_LogEntriesButtonClicked.connect(self.main_window.input_frame.log_entries)
        self.sd.SIG_ShowVideoWindow.connect(self.video_window.show)
        print("4 Signals and Slots connected")

    def undo(self):
        self.sd.SIG_DebugMessage.emit("Undo")

if __name__ == "__main__":
    Main()
