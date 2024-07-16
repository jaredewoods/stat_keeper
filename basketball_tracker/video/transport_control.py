from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize, Qt

class TransportControl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
            ('rewind', 'rewind.png', 'rewind_hover.png', 'rewind_pressed.png', 'rewind_on.png', False),
            ('reverse', 'reverse.png', 'reverse_hover.png', 'reverse_pressed.png', 'reverse_on.png', False),
            ('pause', 'pause.png', 'pause_hover.png', 'pause_pressed.png', 'pause_on.png', False),
            ('capture', 'capture.png', 'capture_hover.png', 'capture_pressed.png', 'capture_on.png', False),
            ('play', 'play.png', 'play_hover.png', 'play_pressed.png', 'play_on.png', False),
            ('forward', 'forward.png', 'forward_hover.png', 'forward_pressed.png', 'forward_on.png', False),
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

            btn.enterEvent = lambda event, b=btn, h=button[2]: b.setIcon(QIcon(h))
            btn.leaveEvent = lambda event, b=btn, o=button[1], on=button[4]: b.setIcon(QIcon(on) if b.state else QIcon(o))
            btn.mousePressEvent = lambda event, b=btn, p=button[3]: b.setIcon(QIcon(p))
            btn.mouseReleaseEvent = lambda event, b=btn, o=button[1], on=button[4]: self.on_release(event, b, o, on)

            self.button_widgets.append(btn)
            layout.addWidget(btn)

        self.setWindowTitle('Transport Control')
        self.setGeometry(300, 300, 800, 100)

    def on_release(self, event, button, off_icon, on_icon):
        if event.button() == Qt.MouseButton.LeftButton:
            button.state = not button.state
            button.setIcon(QIcon(on_icon) if button.state else QIcon(off_icon))

if __name__ == '__main__':
    app = QApplication([])
    ex = TransportControl()
    ex.show()
    app.exec()
