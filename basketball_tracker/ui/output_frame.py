import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTextEdit, QFrame, QCheckBox,
                             QPushButton, QTreeWidget, QTreeWidgetItem, QTabWidget, QTableWidget, QTableWidgetItem)


class OutputFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.tabs = QTabWidget(self)

        self.setup_event_log_tab()
        self.setup_database_tab()
        self.setup_stats_tab()
        self.setup_help_tab()

        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

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

        self.table_widget = QTableWidget(self.database_tab)
        layout.addWidget(self.table_widget)

        self.load_database_data()

        self.database_tab.setLayout(layout)
        self.tabs.addTab(self.database_tab, "Database")

    def load_database_data(self):
        connection = sqlite3.connect('data/player_stats.sqlite')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM player_stats")
        data = cursor.fetchall()
        headers = [description[0] for description in cursor.description]

        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        connection.close()

    def setup_stats_tab(self):
        self.stats_tab = QWidget()
        layout = QVBoxLayout(self.stats_tab)

        self.stats_label = QLabel("stats will go here", self.stats_tab)
        layout.addWidget(self.stats_label)

        self.stats_tab.setLayout(layout)
        self.tabs.addTab(self.stats_tab, "Stats")

    def setup_help_tab(self):
        self.help_tab = QWidget()
        layout = QVBoxLayout(self.help_tab)

        self.help_text = QTextEdit(self.help_tab)
        self.help_text.setPlainText(
            "Event Codes:\n"
            "M3P - Missed 3-pointer\n"
            "3-P - 3-pointer Made\n"
            "DRB - Defensive Rebound\n"
            "STL - Steal\n"
            "F-T - Free Throw Made\n"
            "POI - Play of Interest \n"
            "M2P - Missed 2-pointer\n"
            "ORB - Offensive Rebound\n"
            "2-P - 2-pointer Made\n"
        )
        self.help_text.setReadOnly(True)
        layout.addWidget(self.help_text)

        self.help_tab.setLayout(layout)
        self.tabs.addTab(self.help_tab, "Help")


"""# Example usage
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QVBoxLayout

    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)
    output_frame = OutputFrame()
    layout.addWidget(output_frame)
    window.setLayout(layout)
    window.show()
    app.exec()
"""