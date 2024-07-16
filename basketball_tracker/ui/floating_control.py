from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QHBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont
import sys
import os
from data.rosters_dao import RostersDAO
from data.events_dao import EventsDAO

script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, '../images/')


class FloatingControl(QWidget):
    def __init__(self, signal_distributor=None, state_manager=None):
        super().__init__()
        self.sd = signal_distributor
        self.sm = state_manager
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.rosters_dao = RostersDAO()
        self.events_dao = EventsDAO()

        main_layout = QVBoxLayout(self)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent; border: none;")
        main_layout.addWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.create_page_1())
        self.stacked_widget.addWidget(self.create_page_2())
        self.stacked_widget.addWidget(self.create_page_3())
        self.stacked_widget.addWidget(self.create_page_4())
        self.stacked_widget.setCurrentIndex(0)

        nav_layout = QHBoxLayout()
        prev_button = self.create_nav_button('left_arrow')
        next_button = self.create_nav_button('right_arrow')
        prev_button.clicked.connect(self.show_previous_page)
        next_button.clicked.connect(self.show_next_page)
        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(next_button)

        # main_layout.addLayout(nav_layout)


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
        capture_button.clicked.connect(self.capture_button_clicked)
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
        undo_button.clicked.connect(self.undo_button_clicked)
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
        font = QFont("Arial", 22)
        roster_list = QListWidget()
        roster_list.setFont(font)
        roster_list.setStyleSheet("""
            QListWidget::item {
                color: white;
                background: transparent;
                height: 40px;
            }
            QListWidget::item:hover {
                color: black;
                background: lightgrey;
            }
            QListWidget::item:selected {
                color: blue;
                background: white;
            }
            """)

        roster_data = self.rosters_dao.fetch_roster_sans_headers()
        for player in roster_data:
            item = QListWidgetItem(f"{player[0]} {player[1]} {player[2]}")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            roster_list.addItem(item)

        roster_list.itemClicked.connect(self.player_selected)
        layout.addWidget(roster_list)
        page.setLayout(layout)
        return page

    def create_page_3(self):
        page = QWidget()
        page.setStyleSheet(f"""
            QWidget {{
                background-image: url({os.path.join(images_dir, 'basketballs.png')});
                background-repeat: no-repeat;
                background-position: center;
            }}
        """)
        layout = QVBoxLayout(page)
        font = QFont("Arial", 22)
        events_list = QListWidget()
        events_list.setFont(font)
        events_list.setStyleSheet("""
            QListWidget::item {
                color: white;
                background: transparent;
            }
            QListWidget::item:hover {
                color: black;
                background: lightgrey;
            }
            QListWidget::item:selected {
                color: blue;
                background: white;
            }
        """)

        events = self.events_dao.fetch_event_descriptions()
        for event in events:
            item = QListWidgetItem(event)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            events_list.addItem(item)

        events_list.itemClicked.connect(self.event_selected)
        layout.addWidget(events_list)
        page.setLayout(layout)
        return page

    def create_page_4(self):
        page = QWidget()
        page.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        layout.addWidget(confirm_button, 0, Qt.AlignmentFlag.AlignCenter)
        confirm_button.clicked.connect(self.confirm_button_clicked)

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
        layout.addWidget(edit_button, 0, Qt.AlignmentFlag.AlignCenter)
        edit_button.clicked.connect(self.edit_button_clicked)

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

    def capture_button_clicked(self):
        self.sd.SIG_CapturePauseButtonClicked.emit()
        self.show_next_page()

    def undo_button_clicked(self):
        self.sd.SIG_DebugMessage.emit("Undo button clicked")

    def player_selected(self, item):
        player = item
        self.sd.SIG_RosterPlayerSelected.emit(player)
        self.show_next_page()

    def event_selected(self, item):
        event_name = item.text()
        self.sd.SIG_EventCodeSelected.emit(event_name)
        self.sd.SIG_DebugMessage.emit(f"Event Selected: {event_name}")
        self.show_next_page()

    def confirm_button_clicked(self):
        self.sd.SIG_LogEntriesButtonClicked.emit()
        self.show_next_page()

    def edit_button_clicked(self):
        self.sd.SIG_DebugMessage.emit("Edit button clicked")
        self.show_next_page()
        self.show_next_page()


# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    floating_control = FloatingControl()
    floating_control.show()
    sys.exit(app.exec())
