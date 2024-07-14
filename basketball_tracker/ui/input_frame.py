from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QFrame, QTabWidget, QListWidget, QListWidgetItem, QApplication
from PyQt6.QtGui import QFont
import sqlite3
from data.rosters_dao import RostersDAO


class InputFrame(QWidget):
    game_info_labels = ["📅 ", "🕐 ", "🏠 ", "🆚 "]
    event_entry_labels = ["⏳ ", "📷 ", "🏃 ", "🏀 "]
    context_labels = ["Full_Game", "1st_Quarter", "2nd_Quarter", "3rd_Quarter", "4th_Quarter", "Overtime",
                      "DBL_Overtime", "1st_Half", "2nd_Half", "5th_Period"]
    label_width = 7

    def __init__(self, parent=None, signal_distributor=None, state_manager=None):
        super().__init__(parent)
        self.roster_list_widget = None
        self.selected_event_code = None
        self.sd = signal_distributor
        self.sm = state_manager
        self.team_roster_frame = None
        self.event_entry_frame = None
        self.player_entry = None
        self.opponent_entry = None
        self.venue_entry = None
        self.start_time_entry = None
        self.date_entry = None
        self.event_entry = None
        self.game_info_frame = None
        self.rosters_dao = RostersDAO()

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)

        self.create_game_info_frame()
        self.create_event_entry_frame()
        self.create_team_roster_frame()
        print("3 InputFrame initialized")

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
            font = QFont("Arial", 16)
            entry.setFont(font)
            row_layout.addWidget(entry)
            layout.addLayout(row_layout)

            if text == "📅 ":
                entry.setText("1/24/82")
                self.date_entry = entry
            elif text == "🕐 ":
                entry.setText("16:30")
                self.start_time_entry = entry
            elif text == "🏠 ":
                entry.setText("United Center")
                self.venue_entry = entry
            elif text == "🆚 ":
                entry.setText("Bulls")
                self.opponent_entry = entry

        self.game_info_frame.setLayout(layout)
        self.tabs.addTab(self.game_info_frame, "Game Info")

    def create_event_entry_frame(self):
        self.event_entry_frame = QWidget()
        layout = QVBoxLayout(self.event_entry_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(5, 0, 5, 0)
        for text in InputFrame.event_entry_labels:
            row_layout = QHBoxLayout()
            label = QLabel(text, self.event_entry_frame)
            font = QFont("Arial", 18)
            label.setFont(font)
            row_layout.addWidget(label)
            if text == "⏳":
                entry = QComboBox(self.event_entry_frame)
                entry.addItems(InputFrame.context_labels)
                entry.setCurrentText("Full_Game")
            else:
                entry = QLineEdit(self.event_entry_frame)
                entry.setFixedHeight(30)
                font = QFont("Arial", 16)
                entry.setFont(font)
                if text == "🏀 ":
                    self.event_entry = entry  # Store reference to the "Event" QLineEdit
                elif text == "🏃 ":
                    self.player_entry = entry  # Store reference to the "Player" QLineEdit
            row_layout.addWidget(entry)
            layout.addLayout(row_layout)

        self.event_entry_frame.setLayout(layout)
        self.tabs.addTab(self.event_entry_frame, "Event Entry")

    def create_team_roster_frame(self):
        self.team_roster_frame = QFrame(self)
        self.team_roster_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self.team_roster_frame)

        self.roster_list_widget = QListWidget(self.team_roster_frame)
        roster_data = self.rosters_dao.fetch_roster_sans_headers()
        for player in roster_data:
            player_name = f"{player[0]}  {player[1]} {player[2]}"
            QListWidgetItem(player_name, self.roster_list_widget)

        self.roster_list_widget.itemClicked.connect(self.player_selected)
        layout.addWidget(self.roster_list_widget)

        self.team_roster_frame.setLayout(layout)
        self.layout().addWidget(self.team_roster_frame)
        
    def player_selected(self, item):
        player_name = item.text()
        if self.player_entry:
            self.player_entry.setText(player_name)
            self.sd.SIG_DebugMessage.emit(f"Player selected: {player_name}")

    def event_code_selected(self, code):
        self.selected_event_code = code
        self.sd.SIG_DebugMessage.emit(f"Selected event code {self.selected_event_code}")
        if self.event_entry:
            self.event_entry.setText(self.selected_event_code)

# Test the InputFrame
if __name__ == "__main__":
    app = QApplication([])
    window = InputFrame()
    window.show()
    app.exec()
