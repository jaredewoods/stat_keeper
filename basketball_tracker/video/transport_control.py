from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt, QEvent
import os


class TransportControl(QMainWindow):
    def __init__(self, signal_distributor=None, state_manager=None):
        super().__init__()
        self.buttons = None
        self.button_widgets = None
        self.sd = signal_distributor
        self.sm = state_manager
        self.initUI()

    def initUI(self):
        # Ensure working directory is set correctly
        base_dir = os.path.dirname(os.path.abspath(__file__))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        # Set background color and raised appearance for central widget
        central_widget.setStyleSheet("""
            background-color: black;
            border: 2px solid #555;
            border-radius: 10px;
            padding: 10px;
        """)

        # Button configurations
        self.buttons = [
            ('rewind', os.path.join(base_dir, 'transport_images/rewind.png'), self.rewind_action),
            ('reverse', os.path.join(base_dir, 'transport_images/reverse.png'), self.reverse_action),
            ('pause', os.path.join(base_dir, 'transport_images/pause.png'), self.pause_action),
            ('capture', os.path.join(base_dir, 'transport_images/record.png'), self.capture_action),
            ('play', os.path.join(base_dir, 'transport_images/play.png'), self.play_action),
            ('forward', os.path.join(base_dir, 'transport_images/forward.png'), self.forward_action),
        ]

        self.button_widgets = []

        for button in self.buttons:
            btn = QPushButton()
            btn.setIcon(QIcon(button[1]))
            btn.setIconSize(QSize(100, 100))
            btn.setObjectName(button[0])
            btn.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    border: 2px solid #555;
                    border-radius: 10px;
                    padding: 5px;
                }
                QPushButton:hover {
                    border-color: #888;
                }
                QPushButton:pressed {
                    background-color: #222;
                }
            """)  # To remove button borders and add styles
            btn.state = False  # Initial state is off

            # Simplified event handlers
            btn.enterEvent = self.create_event_handler(btn, button[1].replace('.png', '_hover.png'))
            btn.leaveEvent = self.create_event_handler(btn, button[1], button[1].replace('.png', '_on.png'))
            btn.mousePressEvent = self.create_event_handler(btn, button[1].replace('.png', '_pressed.png'))
            btn.mouseReleaseEvent = self.create_event_handler(btn, button[1], button[1].replace('.png', '_on.png'),
                                                              True, action=button[2])

            self.button_widgets.append(btn)
            layout.addWidget(btn)

        self.setWindowTitle('Transport Control')
        self.setGeometry(300, 300, 800, 100)

    @staticmethod
    def create_event_handler(button, icon_path, on_icon_path=None, toggle_state=False, action=None):
        def handler(event):
            if toggle_state and event.button() == Qt.MouseButton.LeftButton:
                button.state = not button.state

            # Call the associated action if provided
            if action and event.type() == QEvent.Type.MouseButtonRelease:
                action()

            button.setIcon(QIcon(on_icon_path if button.state and on_icon_path else icon_path))

        return handler

    def rewind_action(self):
        self.sd.SIG_DebugMessage.emit("Back20ButtonClicked")
        self.sd.SIG_Back20ButtonClicked.emit()

    def reverse_action(self):
        self.sd.SIG_DebugMessage.emit("SIG_Back10ButtonClicked")
        self.sd.SIG_Back10ButtonClicked.emit()

    def pause_action(self):
        self.sd.SIG_DebugMessage.emit("PauseButtonClicked")
        self.sd.SIG_PauseButtonClicked.emit()

    def capture_action(self):
        self.sd.SIG_DebugMessage.emit("CaptureButtonClicked")
        self.sd.SIG_CaptureButtonClicked.emit()

    def play_action(self):
        self.sd.SIG_DebugMessage.emit("PlayButtonClicked")
        self.sd.SIG_PlayButtonClicked.emit()

    def forward_action(self):
        self.sd.SIG_ChangePlaybackSpeedButtonClicked.emit()
        self.sd.SIG_DebugMessage.emit("ChangePlaybackSpeedButtonClicked")


if __name__ == '__main__':
    app = QApplication([])
    ex = TransportControl()
    ex.show()
    app.exec()
