import sqlite3
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTextEdit, QFrame, QCheckBox,
                             QPushButton, QTreeWidget, QTreeWidgetItem, QTabWidget, QTableWidget, QTableWidgetItem)


class OutputFrame(QWidget):
    def __init__(self, parent=None, signal_distributor=None, state_manager=None, player_stats_dao=None):
        super().__init__(parent)
        self.event_log_text = None
        self.debug_display = None
        self.sd = signal_distributor
        self.sm = state_manager
        self.dao = player_stats_dao
        self.events_tab = QWidget()
        self.roster_tab = QWidget()
        self.stats_tab = QWidget()
        self.raw_stats_tab = None
        self.tabs = None
        self.event_log_tab = None
        self.debug_log_tab = None
        self.stats_tab = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget(self)

        self.setup_debug_log_tab()
        self.setup_event_log_tab()
        self.setup_raw_stats_tab()
        self.setup_roster_tab()
        self.setup_events_tab()
        self.setup_stats_tab()

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    # Debug Tab
    def setup_debug_log_tab(self):
        self.debug_log_tab = QWidget()
        layout = QVBoxLayout(self.debug_log_tab)
        self.debug_display = QTextEdit(self.debug_log_tab)
        self.debug_display.setReadOnly(True)
        self.debug_display.append("DebugLogDisplay Initialized")
        layout.addWidget(self.debug_display)
        self.debug_log_tab.setLayout(layout)
        self.tabs.addTab(self.debug_log_tab, "🔲 Debug Log")

    @pyqtSlot(str)
    def append_debug_message(self, message):
        self.debug_display.append(message)

    # Event Tab
    def setup_event_log_tab(self):
        self.event_log_tab = QWidget()
        layout = QVBoxLayout(self.event_log_tab)
        self.event_log_text = QTextEdit(self.event_log_tab)
        self.event_log_text.setPlainText("Logged events display below:")
        self.event_log_text.setReadOnly(True)
        layout.addWidget(self.event_log_text)
        self.event_log_tab.setLayout(layout)
        self.tabs.addTab(self.event_log_tab, "🔲 Event Log")

    @pyqtSlot(dict)
    def append_event_log(self, data):
        log_entry = (f"{data['date']},{data['time']},{data['venue']},{data['opponent']},"
                     f"{data['context']},{data['timecode']},{data['player']},{data['event']}")
        self.event_log_text.append(log_entry)

    # Raw Stats Tab
    def setup_raw_stats_tab(self):
        self.raw_stats_tab = QWidget()
        layout = QVBoxLayout(self.raw_stats_tab)
        raw_stats_table_widget = QTableWidget(self.raw_stats_tab)
        layout.addWidget(raw_stats_table_widget)
        self.load_raw_stats_tab(raw_stats_table_widget)
        self.raw_stats_tab.setLayout(layout)
        self.tabs.addTab(self.raw_stats_tab, "🔲 Raw Stats")

    def load_raw_stats_tab(self, table_widget):
        headers, data = self.dao.fetch_raw_stats()
        self.populate_table_widget(table_widget, headers, data)

    @pyqtSlot()
    def refresh_raw_stats_tab(self):
        table_widget = self.raw_stats_tab.findChild(QTableWidget)
        if table_widget:
            self.load_raw_stats_tab(table_widget)
        table_widget.scrollToBottom()

    # Roster Tab
    def setup_roster_tab(self):
        self.roster_tab = QWidget()
        layout = QVBoxLayout(self.roster_tab)
        roster_table_widget = QTableWidget(self.roster_tab)
        layout.addWidget(roster_table_widget)
        self.load_roster_tab(roster_table_widget)
        self.roster_tab.setLayout(layout)
        self.tabs.addTab(self.roster_tab, "🔲 Roster")

    def load_roster_tab(self, table_widget):
        headers, data = self.dao.fetch_roster()
        self.populate_table_widget(table_widget, headers, data)

    # Events Tab
    def setup_events_tab(self):
        layout = QVBoxLayout(self.events_tab)
        events_table_widget = QTableWidget(self.events_tab)
        layout.addWidget(events_table_widget)
        self.load_events_tab(events_table_widget)
        self.events_tab.setLayout(layout)
        self.tabs.addTab(self.events_tab, "🔲 Events")

    def load_events_tab(self, table_widget):
        headers, data = self.dao.fetch_events()
        self.populate_table_widget(table_widget, headers, data)

    # Stats Tab
    def setup_stats_tab(self):
        self.stats_tab = QWidget()
        layout = QVBoxLayout(self.stats_tab)
        stats_table_widget = QTableWidget(self.stats_tab)
        layout.addWidget(stats_table_widget)
        self.load_stats_tab(stats_table_widget)
        self.stats_tab.setLayout(layout)
        self.tabs.addTab(self.stats_tab, "🔲 Stats")

    def load_stats_tab(self, table_widget):
        headers, data = self.dao.fetch_processed_stats()
        self.populate_table_widget(table_widget, headers, data)

    @pyqtSlot()
    def refresh_stats_tab(self):
        table_widget = self.stats_tab.findChild(QTableWidget)
        if table_widget:
            self.load_stats_tab(table_widget)
        table_widget.scrollToBottom()

    # Helper
    @staticmethod
    def populate_table_widget(table_widget, headers, data):
        table_widget.clear()
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        table_widget.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                # print(f"Setting item at row {row_idx}, col {col_idx}: {col_data}")  # Debugging print
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        table_widget.resizeColumnsToContents()
        if headers and data:
            table_widget.scrollToItem(table_widget.item(table_widget.rowCount() - 1, 0))
