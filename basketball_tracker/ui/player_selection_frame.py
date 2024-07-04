# player_selection_frame.py

import csv

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QListWidget, QListWidgetItem


class PlayerSelectionFrame(QWidget):
    def __init__(self, roster_csv_path):
        super().__init__()
        self.roster_csv_path = roster_csv_path
        self.listWidget = None
        self.setWindowTitle("Select a Player")
        self.setGeometry(400, 100, 300, 500)
        self.init_ui()

    def init_ui(self):
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(0, 0, 300, 500)
        self.listWidget.setStyleSheet("""
            QListWidget {
                font-size: 24px;
            }
            QListWidget::item {
                padding: 9px;
                border-radius: 5px;
                text-align: center;
            }
            QListWidget::item:hover {
                background-color: darkBlue;
            }
            QListWidget::item:selected {
                background-color: darkRed;
                color: white;
            }
        """)
        self.populate_list_from_csv()
        self.listWidget.itemClicked.connect(self.on_item_clicked)

    def populate_list_from_csv(self):
        with open(self.roster_csv_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                if len(row) >= 3:
                    item_text = f"{row[0]} {row[1]} {row[2]}"
                    item = QListWidgetItem(item_text)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.listWidget.addItem(item)

    @staticmethod
    def on_item_clicked(item):
        self.sd.SIG_DebugMessage.emit(f"Selected player: {item.text()}")