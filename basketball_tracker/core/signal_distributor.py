# signal_distributor.py

from PyQt6.QtCore import QObject, pyqtSignal


class SignalDistributor(QObject):

    SIG_DebugMessage = pyqtSignal(str)
    SIG_CaptureButtonClicked = pyqtSignal()
    SIG_RosterPlayerSelected = pyqtSignal(str)
    SIG_EventCodeSelected = pyqtSignal(str)
    SIG_UndoButtonClicked = pyqtSignal()


    print("1 SignalDistributor Initialized")
