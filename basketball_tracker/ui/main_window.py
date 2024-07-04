# main_window.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self, signal_distributor, state_manager):
        super().__init__()
        self.sd = signal_distributor
        self.sm = state_manager

        self.setWindowTitle("Basketball Statistics Tracker")
        self.setGeometry(100, 100, 800, 600)

        # Set up central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        print("4 MainWindow Initialized")

# Test the MainWindow
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
