from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint
import sqlite3
import sys
import os

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

# Page 1: Capture and Undo Buttons
def create_page_1():
    page = QWidget()
    page.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(page)
    capture_button = create_button('capture')
    undo_button = create_button('undo')
    layout.addWidget(capture_button)
    layout.addWidget(undo_button)
    return page

# Page 2: Player Roster
def create_page_2():
    page = QWidget()
    page.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(page)

    def get_roster_data():
        connection = sqlite3.connect(os.path.join(script_dir, '../data/Rosters.sqlite'))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM RMHS_roster")
        roster_data = cursor.fetchall()
        connection.close()
        return roster_data

    roster_data = get_roster_data()
    for player in roster_data:
        player_label = QLabel(f"{player[0]} - {player[1]} - {player[2]}")
        player_label.setStyleSheet("color: white;")  # Set text color to white or any other color for visibility
        layout.addWidget(player_label)

    return page

# Page 3: Event Descriptions
def create_page_3():
    page = QWidget()
    page.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(page)
    # Mock event descriptions for testing
    events = ["Event 1: Description", "Event 2: Description", "Event 3: Description"]
    for event in events:
        label = QLabel(event)
        label.setStyleSheet("color: white;")  # Set text color to white or any other color for visibility
        layout.addWidget(label)
    return page

# Page 4: Confirm and Undo Buttons
def create_page_4():
    page = QWidget()
    page.setStyleSheet("background: transparent;")
    layout = QVBoxLayout(page)
    confirm_button = create_button('confirm')
    edit_button = create_button('edit')
    layout.addWidget(confirm_button)
    layout.addWidget(edit_button)
    return page

# Main Control Frame
class FloatingControl(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # Remove window frame
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Set window background to transparent

        main_layout = QVBoxLayout(self)

        # Create the stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent;")
        main_layout.addWidget(self.stacked_widget)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(create_page_1())
        self.stacked_widget.addWidget(create_page_2())
        self.stacked_widget.addWidget(create_page_3())
        self.stacked_widget.addWidget(create_page_4())

        self.stacked_widget.setCurrentIndex(0)  # Start with the first page

        # Navigation buttons
        nav_layout = QHBoxLayout()
        prev_button = create_nav_button('left_arrow')
        next_button = create_nav_button('right_arrow')
        prev_button.clicked.connect(self.show_previous_page)
        next_button.clicked.connect(self.show_next_page)
        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(next_button)

        main_layout.addLayout(nav_layout)

        # Variables to track dragging
        self.old_pos = QPoint()

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
