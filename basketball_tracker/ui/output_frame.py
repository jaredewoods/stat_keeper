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
            "1/24/82,16:30,United Center,Bulls,Full Game,03:37.24,Bakou,Isaac,M3P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,04:06.21,Bolf,Will,3-P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,10:24.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,01:20.21,Lang,Oliver,STL\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,02:31.21,Bolf,Will,F-T\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,04:28.10,Bolf,Will,DRB\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,08:13.10,Towle,Declan,3-P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,10:38.11,Samuels,Zach,POI\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,44:00.11,Samuels,Zach,POI\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,09:39.18,Klimek,Jack,M2P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,01:28.18,Klimek,Jack,M2P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,10:22.30,Lang,Oliver,STL\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,00:17.11,Samuels,Zach,ORB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:56.23,Towle,Declan,3-P\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,00:45.30,Klimek,Jack,2-P\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,ORB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
        )
        self.event_log_text.setReadOnly(True)
        layout.addWidget(self.event_log_text)

        self.event_log_tab.setLayout(layout)
        self.tabs.addTab(self.event_log_tab, "Log")

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
        self.debug_display.append("DebugLogDisplay Initialized.\n")

        layout.addWidget(self.debug_display)
        self.debug_log_tab.setLayout(layout)
        self.tabs.addTab(self.debug_log_tab, "Debug Log")

    @pyqtSlot(str)
    def append_debug_message(self, message):
        self.debug_display.append(message)

