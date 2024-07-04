import sys
import csv
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor


class RoundButton(QPushButton):
    def __init__(self, color, hover_color, pressed_color, text, parent=None):
        super().__init__(parent)
        self.default_color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.text = text
        self.init_ui()

    def init_ui(self):
        self.setText(self.text)
        self.setFixedSize(QSize(200, 200))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setStyleSheet(self.get_style(self.default_color, self.hover_color))
        self.pressed.connect(self.on_pressed)
        self.released.connect(self.on_released)

    def get_style(self, color, hover_color):
        return f"""
        QPushButton {{
            background-color: {color};
            border-radius: 100px;
            font-size: 24px;
            font-weight: bold;
            color: white;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        QPushButton:pressed {{
            background-color: {self.pressed_color};
        }}
        """

    def on_pressed(self):
        self.setStyleSheet(self.get_style(self.pressed_color, self.hover_color))

    def on_released(self):
        self.setStyleSheet(self.get_style(self.default_color, self.hover_color))

class PlayerSelectionFrame(QWidget):
    def __init__(self, csv_file_path=None):
        super().__init__()
        self.csv_file_path = csv_file_path
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
        with open(self.csv_file_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                if len(row) >= 3:
                    item_text = f"{row[0]} {row[1]} {row[2]}"
                    item = QListWidgetItem(item_text)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.listWidget.addItem(item)

    def on_item_clicked(self, item):
        print(f"Selected player: {item.text()}")  # Placeholder for actual functionality


class FloatingControls(QWidget):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Floating Controls")
        self.setGeometry(400, 100, 300, 500)

        # Load configuration
        self.config = ConfigManager()

        # Create layout and buttons
        self.layout = QVBoxLayout()
        self.capture_button = RoundButton("blue", "lightblue", "darkblue", "CAPTURE")
        self.undo_button = RoundButton("red", "lightcoral", "darkred", "UNDO")

        # Add buttons to layout
        self.layout.addWidget(self.capture_button)
        self.layout.addWidget(self.undo_button)

        self.setLayout(self.layout)

        # Connect buttons to actions
        self.capture_button.clicked.connect(self.show_player_selection)

    def show_player_selection(self):
        roster_path = self.config.get(ConfigManager.ROSTER_CSV_PATH)
        self.player_selection_frame = PlayerSelectionFrame(csv_file_path=roster_path)
        self.player_selection_frame.show()

# Test the FloatingControls window
if __name__ == "__main__":
    app = QApplication([])
    window = FloatingControls()
    window.show()
    app.exec()
