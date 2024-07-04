# main_window.py
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QVBoxLayout, QWidget
from floating_controls import FloatingControls  # Import the FloatingControls class from its module

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basketball Statistics Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Set up central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Set up menu
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Add File menu
        file_menu = self.menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Add Tools menu
        tools_menu = self.menu_bar.addMenu("Tools")
        open_floating_controls_action = QAction("Open Floating Controls", self)
        open_floating_controls_action.triggered.connect(self.open_floating_controls)
        tools_menu.addAction(open_floating_controls_action)

        self.floating_controls = None

    def open_floating_controls(self):
        if self.floating_controls is None:
            self.floating_controls = FloatingControls()
        self.floating_controls.show()

# Test the MainWindow
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
