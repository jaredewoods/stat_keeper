from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt, QPoint
import sys
import os
from data.rosters_dao import RostersDAO
from data.events_dao import EventsDAO

# Set up the paths for images
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, '../images/')


class ShadowLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Arial", 18))
        self.setStyleSheet("color: white;")
        self.setGraphicsEffect(self.create_shadow_effect())

    def create_shadow_effect(self):
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(4)
        effect.setColor(QColor(0, 0, 0))
        effect.setOffset(3, 3)
        return effect

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

        # Apply a transparent background to the stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(self.stacked_widget)

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.create_page_1())
        self.stacked_widget.addWidget(self.create_page_2())
        self.stacked_widget.addWidget(self.create_page_3())
        self.stacked_widget.addWidget(self.create_page_4())

        self.stacked_widget.setCurrentIndex(0)

        # Create navigation layout with buttons
        nav_layout = QHBoxLayout()
        prev_button = self.create_nav_button('left_arrow')
        next_button = self.create_nav_button('right_arrow')
        prev_button.clicked.connect(self.show_previous_page)
        next_button.clicked.connect(self.show_next_page)
        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(next_button)

        main_layout.addLayout(nav_layout)

        self.old_pos = QPoint()

    def create_page_1(self):
        page = QWidget()
        page.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the layout

        capture_button = QPushButton()
        capture_button.setStyleSheet(f"""
            QPushButton {{
                border-image: url({os.path.join(images_dir, 'capture_dim.png')});
                border-radius: 100px;
                background: transparent;
            }}
            QPushButton:hover {{
                border-image: url({os.path.join(images_dir, 'capture_hover.png')});
            }}
            QPushButton:pressed {{
                border-image: url({os.path.join(images_dir, 'capture_pressed.png')});
            }}
        """)
        capture_button.setFixedSize(200, 200)
        layout.addWidget(capture_button, 0, Qt.AlignmentFlag.AlignCenter)  # Center the button

        undo_button = QPushButton()
        undo_button.setStyleSheet(f"""
            QPushButton {{
                border-image: url({os.path.join(images_dir, 'undo_dim.png')});
                border-radius: 100px;
                background: transparent;
            }}
            QPushButton:hover {{
                border-image: url({os.path.join(images_dir, 'undo_hover.png')});
            }}
            QPushButton:pressed {{
                border-image: url({os.path.join(images_dir, 'undo_pressed.png')});
            }}
        """)
        undo_button.setFixedSize(200, 200)
        layout.addWidget(undo_button, 0, Qt.AlignmentFlag.AlignCenter)  # Center the button

        return page

    def create_page_2(self):
        page = QWidget()
        page.setStyleSheet(f"""
            QWidget {{
                background-image: url({os.path.join(images_dir, 'basketballs.png')});
                background-repeat: no-repeat;
                background-position: center;
                border: none;
            }}
        """)
        layout = QVBoxLayout(page)

        roster_data = self.rosters_dao.get_all_roster_data()
        for player in roster_data:
            player_label = ShadowLabel(f"{player[0]} {player[1]} {player[2]}")
            player_label.setStyleSheet("color: white; background: transparent; border: none; font-weight: bold")
            player_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the layout
            layout.addWidget(player_label)

        return page

    def create_page_3(self):
        page = QWidget()
        page.setStyleSheet(f"""
            QWidget {{
                background-image: url({os.path.join(images_dir, 'basketballs.png')});
                background-repeat: no-repeat;
                background-position: center;
                border: none;
            }}
        """)
        layout = QVBoxLayout(page)

        events = self.events_dao.get_all_events()
        for event in events:
            label = ShadowLabel(f"{event[0]}: {event[1]}")
            label.setStyleSheet("color: white; background: transparent; border: none;")
            layout.addWidget(label)

        return page

    def create_page_4(self):
        page = QWidget()
        page.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the layout

        confirm_button = QPushButton()
        confirm_button.setStyleSheet(f"""
            QPushButton {{
                border-image: url({os.path.join(images_dir, 'confirm_dim.png')});
                border-radius: 100px;
                background: transparent;
            }}
            QPushButton:hover {{
                border-image: url({os.path.join(images_dir, 'confirm_hover.png')});
            }}
            QPushButton:pressed {{
                border-image: url({os.path.join(images_dir, 'confirm_pressed.png')});
            }}
        """)
        confirm_button.setFixedSize(200, 200)
        layout.addWidget(confirm_button, 0, Qt.AlignmentFlag.AlignCenter)  # Center the button

        edit_button = QPushButton()
        edit_button.setStyleSheet(f"""
            QPushButton {{
                border-image: url({os.path.join(images_dir, 'edit_dim.png')});
                border-radius: 100px;
                background: transparent;
            }}
            QPushButton:hover {{
                border-image: url({os.path.join(images_dir, 'edit_hover.png')});
            }}
            QPushButton:pressed {{
                border-image: url({os.path.join(images_dir, 'edit_pressed.png')});
            }}
        """)
        edit_button.setFixedSize(200, 200)
        layout.addWidget(edit_button, 0, Qt.AlignmentFlag.AlignCenter)  # Center the button

        return page

    def create_nav_button(self, image_name):
        btn = QPushButton()
        btn.setStyleSheet(f"""
            QPushButton {{
                border-image: url({os.path.join(images_dir, image_name + '_dim.png')});
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
