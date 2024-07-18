# signal_distributor.py

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QListWidgetItem

class SignalDistributor(QObject):

    SIG_DebugMessage = pyqtSignal(str)
    SIG_RosterPlayerSelected = pyqtSignal(QListWidgetItem)
    SIG_EventCodeSelected = pyqtSignal(str)

    SIG_BackToZeroButtonClicked = pyqtSignal()
    SIG_Back20ButtonClicked = pyqtSignal()
    SIG_Back10ButtonClicked = pyqtSignal()
    SIG_ChangePlaybackSpeedButtonClicked = pyqtSignal()
    SIG_CaptureButtonClicked = pyqtSignal()
    SIG_PauseButtonClicked = pyqtSignal()
    SIG_UndoButtonClicked = pyqtSignal()
    SIG_PlayButtonClicked = pyqtSignal()
    SIG_LogEntriesButtonClicked = pyqtSignal()
    SIG_ShowVideoWindow = pyqtSignal()
    SIG_TimeUpdate = pyqtSignal(str)
    SIG_EnterCapturedTimecode = pyqtSignal(str)
    print("1 SignalDistributor Initialized")
