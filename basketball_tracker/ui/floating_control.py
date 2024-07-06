from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint
import sqlite3
import sys
import os
from data.rosters_dao import RostersDAO
from data.events_dao import EventsDAO

# Set up the paths for images
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, '../images/')

# Function to create a button with different states
def create_button(image_name):
    btn = QPushButton()
    btn.setStyleSheet(f"""
        QPushButton {{
            border-image: url({os.path.join(images_dir, image_name + '_dim.png')});
            border-radius: 100px;
            background: transparent;
        }}
        QPushButton:hover {{
            border-image: url({os.path.join(images_dir, image_name + '_hover.png')});
        }}
        QPushButton:pressed {{
            border-image: url({os.path.join(images_dir, image_name + '_pressed.png')});
        }}
    """)
    btn.setFixedSize(200, 200)
    return btn

# Function to create navigation buttons with different states
def create_nav_button(image_name):
    btn = QPushButton()
    btn.setStyleSheet(f"""
        QPushButton {{
            border-image: url({os.path.join(images_dir, image_name + '_dim.png')});
            border: none;
            background: transparent;
        }}
        QPushButton:hover {{
            border-image: url({os.path.join(images_dir, image_name + '_hover.png')});
        }}
        QPushButton:pressed {{
            border-image: url({os.path.join(images_dir, image_name + '_pressed.png')});
        }}
    """)
    btn.setFixedSize(80, 56)  # Adjust size as needed
    return btn

class FloatingControl(QWidget):
    def __init__(self, signal_distributor=None, state_manager=None):
        super().__init__()
        self.sd = signal_distributor
        self.sm = state_manager
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.rosters_dao = RostersDAO()  # Initialize RostersDAO
        self.events_dao = EventsDAO()  # Initialize EventsDAO

        main_layout = QVBoxLayout(self)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")
        main_layout.addWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.create_page_1())
        self.stacked_widget.addWidget(self.create_page_2())
        self.stacked_widget.addWidget(self.create_page_3())
        self.stacked_widget.addWidget(self.create_page_4())

        self.stacked_widget.setCurrentIndex(0)

        nav_layout = QHBoxLayout()
        prev_button = create_nav_button('left_arrow')
        next_button = create_nav_button('right_arrow')
        prev_button.clicked.connect(self.show_previous_page)
        next_button.clicked.connect(self.show_next_page)
        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(next_button)

        main_layout.addLayout(nav_layout)

        self.old_pos = QPoint()

    def create_page_1(self):
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(page)
        capture_button = create_button('capture')
        undo_button = create_button('undo')
        layout.addWidget(capture_button)
        layout.addWidget(undo_button)
        return page

    def create_page_2(self):
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(page)

        roster_data = self.rosters_dao.get_all_roster_data()
        for player in roster_data:
            player_label = QLabel(f"{player[0]} - {player[1]} - {player[2]}")
            player_label.setStyleSheet("color: white;")
            layout.addWidget(player_label)

        return page

    def create_page_3(self):
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(page)

        events = self.events_dao.get_all_events()
        for event in events:
            label = QLabel(f"{event[0]}: {event[1]}")
            label.setStyleSheet("color: white;")
            layout.addWidget(label)

        return page

    def create_page_4(self):
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(page)
        confirm_button = create_button('confirm')
        edit_button = create_button('edit')
        layout.addWidget(confirm_button)
        layout.addWidget(edit_button)
        return page

    def show_previous_page(self):
        current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex((current_index - 1) % self.stacked_widget.count())

    def show_next_page(self):
        current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex((current_index + 1) % self.stacked_widget.count())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = QPoint()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    floating_control = FloatingControl()
    floating_control.show()
    sys.exit(app.exec())
