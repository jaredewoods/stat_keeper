import sqlite3
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTextEdit, QFrame, QCheckBox,
                             QPushButton, QTreeWidget, QTreeWidgetItem, QTabWidget, QTableWidget, QTableWidgetItem)
from data.player_stats_dao import PlayerStatsDAO
from data.rosters_dao import RostersDAO
from data.events_dao import EventsDAO


class OutputFrame(QWidget):
    def __init__(self, parent=None, signal_distributor=None, state_manager=None):
        super().__init__(parent)
        self.debug_display = None
        self.sd = signal_distributor
        self.sm = state_manager
        self.events_tab = QWidget()
        self.roster_tab = QWidget()
        self.database_tab = None
        self.tabs = None
        self.event_log_tab = None
        self.debug_log_tab = None
        self.rosters_dao = RostersDAO()
        self.events_dao = EventsDAO()
        self.player_stats_dao = PlayerStatsDAO()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget(self)

        self.setup_debug_log_tab()
        self.setup_event_log_tab()
        self.setup_database_tab()
        self.setup_roster_tab()
        self.setup_events_tab()

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    # noinspection PyAttributeOutsideInit
    def setup_event_log_tab(self):
        self.event_log_tab = QWidget()
        layout = QVBoxLayout(self.event_log_tab)

        self.event_log_text = QTextEdit(self.event_log_tab)
        self.event_log_text.setPlainText(
            "Logged events display below:"
        )
        self.event_log_text.setReadOnly(True)
        layout.addWidget(self.event_log_text)

        self.event_log_tab.setLayout(layout)
        self.tabs.addTab(self.event_log_tab, "Log")

    def append_event_log(self, data):
        # Format the data as needed
        log_entry = (
            f"{data['date']},{data['time']},{data['venue']},{data['opponent']},"
            f"{data['context']},{data['timecode']},{data['player']},{data['event']}\n"
        )
        self.event_log_text.append(log_entry)

    def setup_database_tab(self):
        self.database_tab = QWidget()
        layout = QVBoxLayout(self.database_tab)

        database_table_widget = QTableWidget(self.database_tab)
        layout.addWidget(database_table_widget)

        self.load_database_data(database_table_widget)

        self.database_tab.setLayout(layout)
        self.tabs.addTab(self.database_tab, "Database 🔒")

    def load_database_data(self, table_widget):
        headers, data = self.player_stats_dao.fetch_all_player_stats()

        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def setup_roster_tab(self):
        layout = QVBoxLayout(self.roster_tab)

        roster_table_widget = QTableWidget(self.roster_tab)
        layout.addWidget(roster_table_widget)

        self.load_roster_tab(roster_table_widget)

        self.roster_tab.setLayout(layout)
        self.tabs.addTab(self.roster_tab, "Roster 🔒")

    def load_roster_tab(self, table_widget):
        headers, data = self.rosters_dao.fetch_all_roster()

        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def setup_events_tab(self):
        layout = QVBoxLayout(self.events_tab)

        events_table_widget = QTableWidget(self.events_tab)
        layout.addWidget(events_table_widget)

        self.load_events_tab(events_table_widget)

        self.events_tab.setLayout(layout)
        self.tabs.addTab(self.events_tab, "Events 🔒")

    def load_events_tab(self, table_widget):
        headers, data = self.events_dao.fetch_all_events()

        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def setup_debug_log_tab(self):
        self.debug_log_tab = QWidget()
        layout = QVBoxLayout(self.debug_log_tab)

        self.debug_display = QTextEdit(self.debug_log_tab)
        self.debug_display.setReadOnly(True)
        self.debug_display.append("DebugLogDisplay Initialized")

        layout.addWidget(self.debug_display)
        self.debug_log_tab.setLayout(layout)
        self.tabs.addTab(self.debug_log_tab, "Debug Log")

    @pyqtSlot(str)
    def append_debug_message(self, message):
        self.debug_display.append(message)

