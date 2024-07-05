import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFileDialog
from PyQt6.QtCore import Qt, QTimer

class VideoControlWindow(QMainWindow):
    def __init__(self, video_window):
        super().__init__()
        self.setWindowTitle("Control Window")
        self.setGeometry(200, 100, 400, 300)

        self.video_window = video_window

        # Set up the UI
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.button_layout_1 = QHBoxLayout()
        self.layout.addLayout(self.button_layout_1)

        self.open_button = QPushButton("Open", self)
        self.button_layout_1.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_file)

        self.play_button = QPushButton("Play", self)
        self.button_layout_1.addWidget(self.play_button)
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton("Pause", self)
        self.button_layout_1.addWidget(self.pause_button)
        self.pause_button.clicked.connect(self.pause_video)

        self.reverse_button = QPushButton("Reverse", self)
        self.button_layout_1.addWidget(self.reverse_button)
        self.reverse_button.clicked.connect(self.reverse_video)

        self.button_layout_2 = QHBoxLayout()
        self.layout.addLayout(self.button_layout_2)

        self.normal_speed_button = QPushButton("1x Speed", self)
        self.button_layout_2.addWidget(self.normal_speed_button)
        self.normal_speed_button.clicked.connect(lambda: self.set_playback_rate(1.0))

        self.speed_0_5x_button = QPushButton("0.5x Speed", self)
        self.button_layout_2.addWidget(self.speed_0_5x_button)
        self.speed_0_5x_button.clicked.connect(lambda: self.set_playback_rate(0.5))

        self.speed_2x_button = QPushButton("2x Speed", self)
        self.button_layout_2.addWidget(self.speed_2x_button)
        self.speed_2x_button.clicked.connect(lambda: self.set_playback_rate(2.0))

        self.speed_10x_button = QPushButton("10x Speed", self)
        self.button_layout_2.addWidget(self.speed_10x_button)
        self.speed_10x_button.clicked.connect(lambda: self.set_playback_rate(10.0))

        # Layout for file name and time label
        self.info_layout = QHBoxLayout()
        self.layout.addLayout(self.info_layout)

        self.file_name_label = QLabel("File: None", self)
        self.info_layout.addWidget(self.file_name_label)

        self.time_label = QLabel("Time: 00:00:00 / 00:00:00", self)
        self.info_layout.addWidget(self.time_label)
        self.info_layout.setAlignment(self.time_label, Qt.AlignmentFlag.AlignRight)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.adjustSize()  # Adjust the window size to fit its contents
        self.show()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename:
            self.video_window.open_file(filename)
            # Extract just the file name without the path
            file_name = filename.split('/')[-1]
            self.file_name_label.setText(f"File: {file_name}")

    def play_video(self):
        self.video_window.play_video()

    def pause_video(self):
        self.video_window.pause_video()

    def reverse_video(self):
        self.video_window.reverse_video()

    def set_playback_rate(self, rate):
        self.video_window.set_playback_rate(rate)

    def update_time(self):
        position = self.video_window.get_position() // 1000
        duration = self.video_window.get_duration() // 1000
        self.time_label.setText(f"Time: {self.format_time(position)} / {self.format_time(duration)}")

    @staticmethod
    def format_time(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    from video_window import VideoWindow  # Ensure this import matches your actual module name

    video_window = VideoWindow()
    video_window.show()

    control_window = VideoControlWindow(video_window)
    control_window.show()

    sys.exit(app.exec())
