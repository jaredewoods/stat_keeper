from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap
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
    layout = QVBoxLayout(page)
    capture_button = create_button('capture')
    undo_button = create_button('undo')
    layout.addWidget(capture_button)
    layout.addWidget(undo_button)
    return page

# Page 2: Player Roster
def create_page_2():
    page = QWidget()
    layout = QVBoxLayout(page)
    # Mock roster data for testing
    roster = ["1 John Doe", "2 Jane Smith", "3 Alex Johnson"]
    for player in roster:
        label = QLabel(player)
        layout.addWidget(label)
    return page

# Page 3: Event Descriptions
def create_page_3():
    page = QWidget()
    layout = QVBoxLayout(page)
    # Mock event descriptions for testing
    events = ["Event 1: Description", "Event 2: Description", "Event 3: Description"]
    for event in events:
        label = QLabel(event)
        layout.addWidget(label)
    return page

# Page 4: Confirm and Undo Buttons
def create_page_4():
    page = QWidget()
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
        main_layout = QVBoxLayout(self)

        # Create the stacked widget
        self.stacked_widget = QStackedWidget()
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

    def show_previous_page(self):
        current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex((current_index - 1) % self.stacked_widget.count())

    def show_next_page(self):
        current_index = self.stacked_widget.currentIndex()
        self.stacked_widget.setCurrentIndex((current_index + 1) % self.stacked_widget.count())

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    floating_control = FloatingControl()
    floating_control.show()
    sys.exit(app.exec())
