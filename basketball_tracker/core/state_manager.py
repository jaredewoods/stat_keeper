# state_manager.py

from PyQt6.QtCore import QObject, pyqtSignal


class StateManager(QObject):
    def __init__(self, signal_distributor):
        super().__init__()
        self.sd = signal_distributor

        """Manages and tracks application state using signals."""
        print("2 StateManager Initialized")
