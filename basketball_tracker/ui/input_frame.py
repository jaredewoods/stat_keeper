from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QFrame
from PyQt6.QtCore import Qt


class InputFrame(QWidget):
    game_info_labels = ["Date", "Time", "Venue", "Opponent"]
    event_entry_labels = ["Context", "VideoTime", "Player", "Event"]
    context_labels = ["Full_Game", "1st_Quarter", "2nd_Quarter", "3rd_Quarter", "4th_Quarter", "Overtime",
                      "DBL_Overtime", "1st_Half", "2nd_Half", "5th_Period"]
    label_width = 7

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the main layout for InputFrame
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        self.create_game_info_frame()
        self.create_event_entry_frame()
        self.create_team_roster_frame()
        print("InputFrame initialized")

    def create_game_info_frame(self):
        self.game_info_frame = QFrame(self)
        self.game_info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self.game_info_frame)

        # Labels and Entry Fields
        for text in InputFrame.game_info_labels:
            h_layout = QHBoxLayout()
            label = QLabel(text, self.game_info_frame)
            entry = QLineEdit(self.game_info_frame)
            h_layout.addWidget(label)
            h_layout.addWidget(entry)
            layout.addLayout(h_layout)

            if text == "Date":
                entry.setText("1/24/82")
                self.date_entry = entry
            elif text == "Time":
                entry.setText("16:30")
                self.start_time_entry = entry
            elif text == "Venue":
                entry.setText("United Center")
                self.venue_entry = entry
            elif text == "Opponent":
                entry.setText("Bulls")
                self.opponent_entry = entry

        self.game_info_frame.setLayout(layout)
        self.layout().addWidget(self.game_info_frame)

    def create_event_entry_frame(self):
        self.event_entry_frame = QFrame(self)
        self.event_entry_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self.event_entry_frame)

        self.period_combobox = QComboBox(self.event_entry_frame)
        self.period_combobox.addItems(InputFrame.context_labels)
        self.period_combobox.setCurrentText("Full_Game")
        layout.addWidget(self.period_combobox)

        # Labels and Entry Fields for Event Info
        for text in InputFrame.event_entry_labels:
            h_layout = QHBoxLayout()
            label = QLabel(text, self.event_entry_frame)
            entry = QLineEdit(self.event_entry_frame)
            h_layout.addWidget(label)
            h_layout.addWidget(entry)
            layout.addLayout(h_layout)

            if text == "VideoTime":
                self.video_time_entry = entry
            elif text == "Player":
                self.jersey_number_entry = entry
            elif text == "Event":
                self.event_code_entry = entry

        self.event_entry_frame.setLayout(layout)
        self.layout().addWidget(self.event_entry_frame)

    def create_team_roster_frame(self):
        self.team_roster_frame = QFrame(self)
        self.team_roster_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self.team_roster_frame)

        roster_label = QLabel("TEAM ROSTER", self.team_roster_frame)
        roster_label.setStyleSheet("font: bold 14pt Arial;")
        layout.addWidget(roster_label)

        self.team_roster_frame.setLayout(layout)
        self.layout().addWidget(self.team_roster_frame)

    # Placeholder methods for event handling
    def check_all_fields_filled(self):
        print("Checking all fields...")
        # Placeholder logic

    def display_team_roster(self):
        print("Displaying team roster...")
        # Placeholder logic

    def on_listbox_select(self, event):
        print("Listbox item selected")
        # Placeholder logic

    def update_event_code_entry_and_log(self, data):
        print(f"Updating event code entry with data: {data}")
        # Placeholder logic

    def open_and_load_roster(self):
        print("Opening and loading roster...")
        # Placeholder logic

    def import_roster(self, file_path):
        print(f"Importing roster from {file_path}")
        # Placeholder logic

    def update_video_time_with_quicktime_playtime(self, spinbox_value):
        print(f"Updating video time with QuickTime playtime, spinbox value: {spinbox_value}")
        # Placeholder logic

    def callback_for_ui_data(self, player, event):
        print(f"Callback received Player: {player}, Event: {event}")
        # Placeholder logic
