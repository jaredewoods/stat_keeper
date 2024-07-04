# config_manager.py
import os


class ConfigManager:
    ROSTER_CSV_PATH = "ROSTER_CSV_PATH"
    EVENTS_CSV_PATH = "EVENTS_CSV_PATH"
    BACKUP_TXT_PATH = "BACKUP_TXT_PATH"
    LOGS_FOLDER_PATH = "LOGS_FOLDER_PATH"
    VIDEO_BROWSE_PATH = "VIDEO_BROWSE_PATH"
    DEBUG_MODE_STATE = "DEBUG_MODE_STATE"
    CONFIG_FILE_PATH = "config/config.txt"

    def __init__(self, config_file=None):
        if config_file is None:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_file = os.path.join(base_path, self.CONFIG_FILE_PATH)

        self.config_file = config_file
        self.config = self.read_config()

    def read_config(self):
        config = {}
        with open(self.config_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config

    def get(self, key, default=None):
        return self.config.get(key, default)

# Test the ConfigManager
if __name__ == "__main__":
    config_manager = ConfigManager()
    roster_path = config_manager.get(ConfigManager.ROSTER_CSV_PATH)
    events_path = config_manager.get(ConfigManager.EVENTS_CSV_PATH)
    backup_path = config_manager.get(ConfigManager.BACKUP_TXT_PATH)
    logs_path = config_manager.get(ConfigManager.LOGS_FOLDER_PATH)
    video_browse_path = config_manager.get(ConfigManager.VIDEO_BROWSE_PATH)
    debug_mode = config_manager.get(ConfigManager.DEBUG_MODE_STATE)

    print(f"Roster CSV Path: {roster_path}")
    print(f"Events CSV Path: {events_path}")
    print(f"Backup Text Path: {backup_path}")
    print(f"Logs Folder Path: {logs_path}")
    print(f"Video Browse Path: {video_browse_path}")
    print(f"Debug Mode State: {debug_mode}")
