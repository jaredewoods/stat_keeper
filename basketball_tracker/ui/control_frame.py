# control_frame.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt
from data.events_dao import EventsDAO

BUTTON_FONT = ('Arial', 12, 'bold')

control_button_labels = [
    "<< 00:00", "<< 20s", "<< 10s", "Speed", "VideoTime", "VT+Pause",
    "Pause", "Log", "Play", "Undo"
]


class ControlFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.adjusted_value_label = None
        self.value_spinbox = None
        self.total_time_label = None
        self.omni_button = None
        self.omni_state = "RUN VIDEO"
        self.spin_value = -2  # Initialize with the starting value for the Spinbox
        self.events_dao = EventsDAO()  # Initialize EventsDAO instance
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        self.create_control_buttons(main_layout)
        self.create_status_widgets(main_layout)
        self.create_omni_button(main_layout)
        self.create_action_buttons(main_layout)

        self.setLayout(main_layout)

    def create_control_buttons(self, layout):
        control_layout = QGridLayout()
        for i, button_text in enumerate(control_button_labels):
            button = QPushButton(button_text)
            button.clicked.connect(lambda checked, b=button: self.button_actions.get(b.text(), self.default_action)())
            control_layout.addWidget(button, i // 2, i % 2)
        layout.addLayout(control_layout)

    def create_status_widgets(self, layout):
        _hframe = QHBoxLayout()

        self.total_time_label = QLabel("Loading...", self)
        self.total_time_label.setStyleSheet("font: 14pt Arial; color: #BBBBBB;")
        _hframe.addWidget(self.total_time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.value_spinbox = QSpinBox(self)
        self.value_spinbox.setRange(-59, 0)
        self.value_spinbox.setValue(self.spin_value)
        self.value_spinbox.setStyleSheet("font: 14pt Arial; color: #BBBBBB;")
        _hframe.addWidget(self.value_spinbox, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(_hframe)

    def create_omni_button(self, layout):
        self.omni_button = QPushButton(self.omni_state, self)
        self.omni_button.setStyleSheet("font: 16pt Arial;"
                                       "padding, 10px;"
                                       "border: 2px solid grey;"
                                       "border-radius: 10px;")
        self.omni_button.clicked.connect(self.toggle_omni)
        self.omni_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.omni_button.setFixedHeight(40)
        layout.addWidget(self.omni_button)

    def create_action_buttons(self, layout):
        action_layout = QGridLayout()
        action_button_names = self.events_dao.fetch_event_codes()  # Fetch button names

        for i, name in enumerate(action_button_names):
            button = QPushButton(name)
            button.clicked.connect(lambda checked, n=name: self.set_event_code(n))
            action_layout.addWidget(button, i // 3, i % 3)
        layout.addLayout(action_layout)

    def load_action_button_names(self):
        return self.events_dao.fetch_event_codes()

    @staticmethod
    def undo_action():
        print("Undo")

    @staticmethod
    def default_action():
        print("Default action")

    @staticmethod
    def start_action():
        print("Start action")

    @staticmethod
    def time_capture_action():
        print("Time Capture button pressed")

    @staticmethod
    def tc_and_pause_action():
        print("Time Capture and Pause button pressed")

    @staticmethod
    def pause_action():
        print("Pausing the QuickTime video")

    @staticmethod
    def log_action():
        print("LOG button pressed")

    def toggle_omni(self):
        current_state = self.omni_state
        if current_state == "RUN VIDEO":
            self.omni_state = "CAPTURE TIME"
            self.run_action()
        elif current_state == "CAPTURE TIME":
            self.omni_state = "ENTER LOG"
            self.capture_action()
        elif current_state == "ENTER LOG":
            self.omni_state = "CAPTURE TIME"
            self.enter_action()
        else:
            self.omni_state = "RUN VIDEO"
        self.omni_button.setText(self.omni_state)

    @staticmethod
    def run_action():
        print("Performing the action for RUN state")

    @staticmethod
    def capture_action():
        print("Performing the action for CAPTURE state")

    def enter_action(self):
        self.log_action()
        self.run_action()
        print("Performing the action for ENTER state")

    def set_event_code(self, code):
        print(f"Setting event code {code}")

    @staticmethod
    def rewind_and_play(rewind_seconds):
        print(f"rewindAndPlay{rewind_seconds}")

    @staticmethod
    def update_total_time_label():
        print(f"Failed to get video length: {e}")
