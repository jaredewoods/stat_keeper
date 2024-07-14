# signal_distributor.py

from PyQt6.QtCore import QObject, pyqtSignal


class SignalDistributor(QObject):

    SIG_DebugMessage = pyqtSignal(str)
    SIG_EventCodeSelected = pyqtSignal(str)
    SIG_RosterPlayerSelected = pyqtSignal(str)

    print("1 SignalDistributor Initialized")
