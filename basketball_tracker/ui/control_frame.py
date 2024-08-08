# control_frame.py

from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QSpinBox, QLabel, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont


CONTROL_BUTTON_LABELS = [
    ("🗑️", "clears all tables"),
    ("❌", "Undo last action"),
    ("⏮️", "Reset to zero timecode"),
    ("↩️", "Go back 20 seconds"),
    ("⏪", "Go back 10 seconds"),
    ("⏩", "Change playback speed"),
    ("⏸️", "Pause playback"),
    ("▶️", "Play the video"),
    ("📸", "Capture current frame"),
    ("✅", "Log current entries")
]
class ControlFrame(QWidget):
    def __init__(self, parent=None, signal_distributor=None, state_manager=None, player_stats_dao=None):
        super().__init__(parent)
        self.adjusted_timecode = None
        self.offset_value = None
        self.parsed_timecode = None
        self.sd = signal_distributor
        self.sm = state_manager
        self.dao = player_stats_dao
        self.code = None
        self.adjusted_value_label = None
        self.value_spinbox = None
        self.total_time_label = None
        self.omni_button = None
        self.omni_state = "RUN VIDEO"
        self.spin_value = -2
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.create_control_buttons(main_layout)
        self.create_status_widgets(main_layout)
        self.create_omni_button(main_layout)
        self.create_event_buttons(main_layout)
        self.setLayout(main_layout)

    def create_control_buttons(self, layout):
        control_layout = QGridLayout()

        for i, (name, tooltip) in enumerate(CONTROL_BUTTON_LABELS):
            button = QPushButton(name)
            font = QFont("Arial", 14)
            button.setFont(font)
            button.setFixedHeight(36)
            button.setFixedWidth(80)
            button.setToolTip(tooltip)  # Set the tooltip here
            button.clicked.connect(lambda checked, n=name: self.button_actions(n))
            control_layout.addWidget(button, i // 2, i % 2)
        layout.addLayout(control_layout)

    def create_status_widgets(self, layout):
        status_layout = QHBoxLayout()

        self.total_time_label = QLineEdit("Loading...", self)
        self.total_time_label.setFixedWidth(80)
        self.total_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text inside the QLineEdit
        status_layout.addWidget(self.total_time_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.value_spinbox = QSpinBox(self)
        self.value_spinbox.setRange(-59, 0)
        self.value_spinbox.setValue(self.spin_value)
        self.value_spinbox.setStyleSheet("font: 14pt Arial; color: #BBBBBB;")
        status_layout.addWidget(self.value_spinbox, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(status_layout)

    @pyqtSlot(str)
    def update_time(self, duration):
        self.total_time_label.setText(duration)

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

    def create_event_buttons(self, layout):
        event_layout = QGridLayout()
        event_button_names = self.dao.fetch_events_sans_headers()  # Fetch button names (codes and descriptions)

        for i, (code, description) in enumerate(event_button_names):
            button = QPushButton(code)  # Use the event code as the button text
            button.setToolTip(description)  # Set the tooltip to the event description
            button.clicked.connect(lambda checked, desc=description: self.set_event_code(desc))
            event_layout.addWidget(button, i // 3, i % 3)
        layout.addLayout(event_layout)

    def toggle_omni(self):
        current_state = self.omni_state
        if current_state == "RUN VIDEO":
            self.omni_state = "CAPTURE TIME"
            self.sd.SIG_PlayButtonClicked.emit()
        elif current_state == "CAPTURE TIME":
            self.omni_state = "ENTER LOG"
            self.sd.SIG_CaptureButtonClicked.emit()
            self.sd.SIG_PauseButtonClicked.emit()
        elif current_state == "ENTER LOG":
            self.omni_state = "CAPTURE TIME"
            self.sd.SIG_LogEntriesButtonClicked.emit()
            self.sd.SIG_PlayButtonClicked.emit()
        else:
            self.omni_state = "RUN VIDEO"
        self.omni_button.setText(self.omni_state)

    @pyqtSlot()
    def capture_timecode(self):
        captured_timecode = self.total_time_label.text()
        self.parse_timecode_to_seconds(captured_timecode)

    def parse_timecode_to_seconds(self, timecode):
        hours, minutes, seconds = map(int, timecode.split(':'))
        self.parsed_timecode = (hours * 3600) + (minutes * 60) + seconds
        self.adjust_parsed_timecode_with_offset(self.parsed_timecode)

    def adjust_parsed_timecode_with_offset(self, parsed_timecode):
        self.offset_value = self.value_spinbox.value()
        self.adjusted_timecode = int(parsed_timecode + self.offset_value)
        self.revert_adjusted_timecode_to_time_format(self.adjusted_timecode)

    def revert_adjusted_timecode_to_time_format(self, adjusted_timecode):
        hours = adjusted_timecode // 3600
        minutes = (adjusted_timecode % 3600) // 60
        seconds = adjusted_timecode % 60
        hhmmss = f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}"
        self.sd.SIG_EnterCapturedTimecode.emit(hhmmss)

    def set_event_code(self, code):
        self.code = code
        self.sd.SIG_EventCodeSelected.emit(self.code)

    def button_actions(self, n):
        print("Button clicked: " + n)
        if n == "⏮️":
            self.sd.SIG_BackToZeroButtonClicked.emit()
        if n == "↩️":
            self.sd.SIG_Back20ButtonClicked.emit()
        if n == "⏪":
            self.sd.SIG_Back10ButtonClicked.emit()
        if n == "⏩":
            self.sd.SIG_ChangePlaybackSpeedButtonClicked.emit()
        if n == "📸":
            self.sd.SIG_CaptureButtonClicked.emit()
        if n == "🗑️":
            self.sd.SIG_ClearAllTables.emit()
        if n == "⏸️":
            self.sd.SIG_PauseButtonClicked.emit()
        if n == "❌️":
            self.sd.SIG_UndoButtonClicked.emit()
        if n == "▶️":
            self.sd.SIG_PlayButtonClicked.emit()
        if n == "✅":
            self.sd.SIG_LogEntriesButtonClicked.emit()
