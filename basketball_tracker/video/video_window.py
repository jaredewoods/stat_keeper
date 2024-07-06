import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Window")
        self.setGeometry(100, 100, 800, 600)

        self.media_player = QMediaPlayer(self)
        self.video_widget = QVideoWidget()
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.layout.addWidget(self.video_widget)
        self.media_player.setVideoOutput(self.video_widget)
        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.layout.addWidget(self.position_slider)
        self.show()

    def open_file(self, filename):
        if filename:
            self.media_player.setSource(QUrl.fromLocalFile(filename))
            self.media_player.durationChanged.connect(self.position_slider.setMaximum)
            self.media_player.positionChanged.connect(self.position_slider.setValue)

    def play_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def reverse_video(self):
        current_position = self.media_player.position()
        self.media_player.setPosition(max(0, current_position - 5000))  # Rewind 5 seconds

    def set_playback_rate(self, rate):
        self.media_player.setPlaybackRate(rate)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def get_position(self):
        return self.media_player.position()

    def get_duration(self):
        return self.media_player.duration()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoWindow()
    sys.exit(app.exec())
