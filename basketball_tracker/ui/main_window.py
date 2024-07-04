# main_window.py
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QVBoxLayout, QWidget
import os
from ui.floating_controls import FloatingControls

class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()
        self.setWindowTitle("Basketball Statistics Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Set up central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

# Test the MainWindow
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
