# signal_distributor.py

from PyQt6.QtCore import QObject, pyqtSignal


class SignalDistributor(QObject):
    """Central hub for distributing signals across the application."""

    SIG_DebugMessage = pyqtSignal(str)


