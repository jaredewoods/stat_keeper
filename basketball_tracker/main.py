import os
import sys
from PyQt6.QtWidgets import QApplication
from config.config_manager import ConfigManager
from ui.main_window import MainWindow

def main():
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Set the correct path to the config file
    config_file_path = os.path.join(os.path.dirname(__file__), 'config', 'config.txt')
    config_manager = ConfigManager(config_file=config_file_path)

    # Initialize the main window and other components
    main_window = MainWindow(config_manager=config_manager)
    main_window.show()

    # Start the application's main loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
