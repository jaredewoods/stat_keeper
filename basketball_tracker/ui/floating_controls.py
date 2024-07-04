from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from ui.player_selection_frame import PlayerSelectionFrame
from ui.round_button import RoundButton


class FloatingControls(QWidget):
    def __init__(self, signal_distributor, state_manager, roster_csv_path, events_csv_path):
        super().__init__()
        self.player_selection_frame = None
        self.roster_csv_path = roster_csv_path
        self.events_csv_path = events_csv_path
        self.sd = signal_distributor
        self.sm = state_manager

        self.setWindowTitle("Floating Controls")
        self.setGeometry(400, 100, 300, 500)

        self.layout = QVBoxLayout()
        self.capture_button = RoundButton("blue", "lightblue", "darkblue", "CAPTURE")
        self.undo_button = RoundButton("red", "lightcoral", "darkred", "UNDO")

        self.layout.addWidget(self.capture_button)
        self.layout.addWidget(self.undo_button)

        self.setLayout(self.layout)

        self.capture_button.clicked.connect(self.show_player_selection)

    def show_player_selection(self):
        self.player_selection_frame = PlayerSelectionFrame(self.events_csv_path)
        self.player_selection_frame.show()

    print("5 FloatingControls Initialized")

# Test the FloatingControls window
if __name__ == "__main__":
    app = QApplication([])
    window = FloatingControls()
    window.show()
    app.exec()
