# main_window.py
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt
from ui.control_frame import ControlFrame
from ui.input_frame import InputFrame
from ui.output_frame import OutputFrame

class MainWindow(QMainWindow):
    def __init__(self, signal_distributor, state_manager):
        super().__init__()
        self.sd = signal_distributor
        self.sm = state_manager

        self.setWindowTitle("Basketball Statistics Tracker")
        self.backup_file_path = '../backup.txt'

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.control_frame = ControlFrame(self)
        layout.addWidget(self.control_frame)

        self.input_frame = InputFrame(self)
        layout.addWidget(self.input_frame)

        self.output_frame = OutputFrame(self)
        layout.addWidget(self.output_frame)

        self.adjustSize()
        self.setFixedSize(self.size())

        self.center_window()
        self.update_output_frame_from_file(self.backup_file_path)

    def center_window(self):
        screen_geometry = self.screen().geometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def update_output_frame_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = file.read()
            self.output_frame.update_content(data)
        except FileNotFoundError:
            pass


# Test the MainWindow
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
