from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QFrame, QTabWidget, QListWidget, QListWidgetItem, QApplication
from PyQt6.QtGui import QFont
import sqlite3
from PyQt6.QtCore import Qt, pyqtSlot


class InputFrame(QWidget):
    game_info_labels = ["📅 ", "⏰ ", "🏟 ", "🆚 "]
    event_entry_labels = ["⏳ ", "📸 ", "🏃 ", "🏀 "]
    context_labels = ["Full Game", "1st Quarter", "2nd Quarter", "3rd Quarter", "4th Quarter", "Overtime",
                      "DBL Overtime", "1st Half", "2nd Half", "5th Period"]
    label_width = 7

    def __init__(self, parent=None, signal_distributor=None, state_manager=None, player_stats_dao=None):
        super().__init__(parent)
        self.retrieved_fields = None
        self.context_combobox = None
        self.timecode_entry = None
        self.roster_list_widget = None
        self.selected_event_code = None
        self.sd = signal_distributor
        self.sm = state_manager
        self.dao = player_stats_dao
        self.team_roster_frame = None
        self.event_entry_frame = None
        self.player_entry = None
        self.opponent_entry = None
        self.venue_entry = None
        self.start_time_entry = None
        self.date_entry = None
        self.event_entry = None
        self.game_info_frame = None

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)

        self.create_game_info_frame()
        self.create_event_entry_frame()
        self.create_team_roster_frame()
        print("4 InputFrame initialized")

    def create_game_info_frame(self):
        self.game_info_frame = QWidget()
        layout = QVBoxLayout(self.game_info_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 0, 5, 0)

        for text in InputFrame.game_info_labels:
            row_layout = QHBoxLayout()
            label = QLabel(text, self.game_info_frame)
            row_layout.addWidget(label)
            entry = QLineEdit(self.game_info_frame)
            entry.setFixedHeight(30)
            font = QFont("Arial", 14)
            entry.setFont(font)
            row_layout.addWidget(entry)
            layout.addLayout(row_layout)

            if text == "📅 ":
                entry.setText("1/24/82")
                self.date_entry = entry
            elif text == "⏰ ":
                entry.setText("16:30")
                self.start_time_entry = entry
            elif text == "🏟 ":
                entry.setText("United Center")
                self.venue_entry = entry
            elif text == "🆚 ":
                entry.setText("Bulls")
                self.opponent_entry = entry

        self.game_info_frame.setLayout(layout)
        self.tabs.addTab(self.game_info_frame, "Game Info")

    @pyqtSlot()
    def show_event_entry_tab(self):
        self.tabs.setCurrentIndex(1)

    def create_event_entry_frame(self):
        self.event_entry_frame = QWidget()
        layout = QVBoxLayout(self.event_entry_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 0, 5, 0)
        
        for text in InputFrame.event_entry_labels:
            row_layout = QHBoxLayout()
            label = QLabel(text, self.event_entry_frame)
            row_layout.addWidget(label)
            if text == "⏳ ":
                entry = QComboBox(self.event_entry_frame)
                entry.addItems(InputFrame.context_labels)
                entry.setCurrentText("Full_Game")
                self.context_combobox = entry  # Store reference to the QComboBox
            else:
                entry = QLineEdit(self.event_entry_frame)
                entry.setFixedHeight(30)
                font = QFont("Arial", 14)
                entry.setFont(font)
                if text == "🏀 ":
                    self.event_entry = entry  # Store reference to the "Event" QLineEdit
                elif text == "🏃 ":
                    self.player_entry = entry  # Store reference to the "Player" QLineEdit
                elif text == "📸 ":
                    self.timecode_entry = entry # Store reference to the "Timecode" QLineEdit

            row_layout.addWidget(entry)
            layout.addLayout(row_layout)

        self.event_entry_frame.setLayout(layout)
        self.tabs.addTab(self.event_entry_frame, "Event Entry")

    def create_team_roster_frame(self):
        self.team_roster_frame = QFrame(self)
        self.team_roster_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self.team_roster_frame)

        self.roster_list_widget = QListWidget(self.team_roster_frame)
        roster_data = self.dao.fetch_roster_sans_headers()

        for player in roster_data:
            player_number = player[0]
            if len(str(player_number)) == 1:
                player_number = f"  {player_number}"  # Add a space in front of single-digit numbers

            player_name = f"{player_number}  {player[1]} {player[2]}"
            QListWidgetItem(player_name, self.roster_list_widget)

        self.roster_list_widget.itemClicked.connect(self.player_selected)
        layout.addWidget(self.roster_list_widget)

        self.team_roster_frame.setLayout(layout)
        self.layout().addWidget(self.team_roster_frame)

    # TODO: why won't '@pyqtSlot()' work here?
    def player_selected(self, item):
        player_name = item.text()
        if self.player_entry:
            self.player_entry.setText(player_name)
            self.sd.SIG_DebugMessage.emit(f"Player selected: {player_name}")

    @pyqtSlot(str)
    def event_code_selected(self, code):
        self.selected_event_code = code
        self.sd.SIG_DebugMessage.emit(f"Selected event code {self.selected_event_code}")
        if self.event_entry:
            self.event_entry.setText(self.selected_event_code)

    @pyqtSlot(str)
    def enter_captured_timecode(self, timecode):
        self.timecode_entry.setText(timecode)
        self.sd.SIG_DebugMessage.emit(f"Captured Time: {timecode}")

    @pyqtSlot()
    def log_entries(self):
        self.retrieved_fields = self.retrieve_fields()
        self.sd.SIG_FieldDataRetrieved.emit(self.retrieved_fields)
        self.sd.SIG_DebugMessage.emit(f"Logging Entries\n{self.retrieved_fields}")

    def retrieve_fields(self):
        # Combine all data into a single dictionary
        all_fields = {
            "date": self.date_entry.text(),
            "time": self.start_time_entry.text(),
            "venue": self.venue_entry.text(),
            "opponent": self.opponent_entry.text(),
            "event": self.event_entry.text(),
            "player": self.player_entry.text(),
            "timecode": self.timecode_entry.text(),
            "context": self.context_combobox.currentText()
        }

        return all_fields


if __name__ == "__main__":
    app = QApplication([])
    window = InputFrame()
    window.show()
    app.exec()
