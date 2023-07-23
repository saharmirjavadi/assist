import json

class Settings:
    def __init__(self):
        with open("config.json", "r", encoding="utf-8") as file:
            config_data = json.load(file)
        self.db_url = config_data.get("db_url", "")