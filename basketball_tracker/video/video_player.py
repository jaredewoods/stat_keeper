import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, QTimer

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Video Player")
        self.setGeometry(100, 100, 800, 600)

        # Set up the media player
        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget()

        # Set up the UI
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)

        self.layout.addWidget(self.video_widget)
        self.media_player.setVideoOutput(self.video_widget)

        self.control_layout = QHBoxLayout()
        self.layout.addLayout(self.control_layout)

        self.open_button = QPushButton("Open", self)
        self.control_layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_file)

        self.play_button = QPushButton("Play", self)
        self.control_layout.addWidget(self.play_button)
        self.play_button.clicked.connect(self.play_video)

        self.pause_button = QPushButton("Pause", self)
        self.control_layout.addWidget(self.pause_button)
        self.pause_button.clicked.connect(self.pause_video)

        self.stop_button = QPushButton("Stop", self)
        self.control_layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop_video)

        self.reverse_button = QPushButton("Reverse", self)
        self.control_layout.addWidget(self.reverse_button)
        self.reverse_button.clicked.connect(self.reverse_video)

        self.speed_2x_button = QPushButton("2x Speed", self)
        self.control_layout.addWidget(self.speed_2x_button)
        self.speed_2x_button.clicked.connect(lambda: self.set_playback_rate(2.0))

        self.speed_10x_button = QPushButton("10x Speed", self)
        self.control_layout.addWidget(self.speed_10x_button)
        self.speed_10x_button.clicked.connect(lambda: self.set_playback_rate(10.0))

        self.time_label = QLabel("Time: 00:00:00 / 00:00:00", self)
        self.layout.addWidget(self.time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.show()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename:
            self.media_player.setSource(QUrl.fromLocalFile(filename))
            self.media_player.durationChanged.connect(self.update_time)
            self.media_player.positionChanged.connect(self.update_time)
            self.media_player.setSource(QUrl.fromLocalFile(filename))

    def play_video(self):
        self.media_player.play()
        self.timer.start(1000)

    def pause_video(self):
        self.media_player.pause()
        self.timer.stop()

    def stop_video(self):
        self.media_player.stop()
        self.timer.stop()
        self.time_label.setText("Time: 00:00:00 / 00:00:00")

    def reverse_video(self):
        current_position = self.media_player.position()
        self.media_player.setPosition(max(0, current_position - 5000))  # Rewind 5 seconds

    def set_playback_rate(self, rate):
        self.media_player.setPlaybackRate(rate)

    def update_time(self):
        position = self.media_player.position() // 1000
        duration = self.media_player.duration() // 1000
        self.time_label.setText(f"Time: {self.format_time(position)} / {self.format_time(duration)}")

    @staticmethod
    def format_time(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    sys.exit(app.exec())
