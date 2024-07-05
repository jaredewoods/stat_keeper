from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTextEdit, QFrame, QCheckBox, QPushButton, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtCore import Qt


class OutputFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        self.setup_event_log_frame()
        self.setup_file_management_frame()
        self.setup_sorted_stats_tree()

        self.setLayout(main_layout)

    def setup_event_log_frame(self):
        self.event_log_frame = QFrame(self)
        self.event_log_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self.event_log_frame)

        self.event_log_text = QTextEdit(self.event_log_frame)
        self.event_log_text.setPlainText(
            "1/24/82,16:30,United Center,Bulls,Full Game,03:37.24,Bakou,Isaac,M3P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,04:06.21,Bolf,Will,3-P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,10:24.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,01:20.21,Lang,Oliver,STL\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,02:31.21,Bolf,Will,F-T\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,04:28.10,Bolf,Will,DRB\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,08:13.10,Towle,Declan,3-P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,10:38.11,Samuels,Zach,POI\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,44:00.11,Samuels,Zach,POI\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,09:39.18,Klimek,Jack,M2P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,01:28.18,Klimek,Jack,M2P\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,10:22.30,Lang,Oliver,STL\n"
            "1/24/82,16:30,United Center,Bulls,Full Game,00:17.11,Samuels,Zach,ORB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:56.23,Towle,Declan,3-P\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,00:45.30,Klimek,Jack,2-P\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,ORB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
            "1/24/82,16:30,United Center,Bulls,4th Quarter,01:18.11,Samuels,Zach,DRB\n"
        )
        self.event_log_text.setReadOnly(True)
        layout.addWidget(self.event_log_text)

        self.event_log_frame.setLayout(layout)
        self.layout().addWidget(self.event_log_frame)

    def setup_file_management_frame(self):
        self.file_management_frame = QFrame(self)
        self.file_management_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QGridLayout(self.file_management_frame)

        self.view_checkbox = QCheckBox("View Stats", self.file_management_frame)
        self.view_checkbox.stateChanged.connect(lambda: print("View Stats checkbox toggled"))
        layout.addWidget(self.view_checkbox, 0, 0)

        self.speedbuttons_checkbox = QCheckBox("Speed Buttons", self.file_management_frame)
        self.speedbuttons_checkbox.stateChanged.connect(lambda: print("Speed Buttons checkbox toggled"))
        layout.addWidget(self.speedbuttons_checkbox, 1, 0)

        self.clock_checkbox = QCheckBox("Display Clock", self.file_management_frame)
        self.clock_checkbox.stateChanged.connect(lambda: print("Display Clock checkbox toggled"))
        layout.addWidget(self.clock_checkbox, 0, 1)

        self.controls_checkbox = QCheckBox("Floating Controls", self.file_management_frame)
        self.controls_checkbox.stateChanged.connect(lambda: print("Floating Controls checkbox toggled"))
        layout.addWidget(self.controls_checkbox, 1, 1)

        self.export_button = QPushButton("Export", self.file_management_frame)
        self.export_button.clicked.connect(lambda: print("Export button clicked"))
        layout.addWidget(self.export_button, 0, 2)

        self.import_button = QPushButton("Import", self.file_management_frame)
        self.import_button.clicked.connect(lambda: print("Import button clicked"))
        layout.addWidget(self.import_button, 1, 2)

        self.edit_log_button = QPushButton("Edit Log", self.file_management_frame)
        self.edit_log_button.clicked.connect(lambda: print("Edit Log button clicked"))
        layout.addWidget(self.edit_log_button, 0, 3)

        self.reload_button = QPushButton("Reload", self.file_management_frame)
        self.reload_button.clicked.connect(lambda: print("Reload button clicked"))
        layout.addWidget(self.reload_button, 1, 3)

        self.save_as_button = QPushButton("Save As", self.file_management_frame)
        self.save_as_button.clicked.connect(lambda: print("Save As button clicked"))
        layout.addWidget(self.save_as_button, 0, 4)

        self.quit_button = QPushButton("Quit", self.file_management_frame)
        self.quit_button.clicked.connect(lambda: print("Quit button clicked"))
        layout.addWidget(self.quit_button, 1, 4)

        self.file_management_frame.setLayout(layout)
        self.layout().addWidget(self.file_management_frame)

    def setup_sorted_stats_tree(self):
        self.sorted_stats_frame = QFrame(self)
        self.sorted_stats_frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(self.sorted_stats_frame)

        self.sorted_stats_tree = QTreeWidget(self.sorted_stats_frame)
        layout.addWidget(self.sorted_stats_tree)

        self.sorted_stats_frame.setLayout(layout)
        self.layout().addWidget(self.sorted_stats_frame)

        self.sorted_stats_frame.hide()  # Initially hide the sorted stats frame


# Example usage
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QGridLayout

    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)
    output_frame = OutputFrame()
    layout.addWidget(output_frame)
    window.setLayout(layout)
    window.show()
    app.exec()
