from configparser import ConfigParser


class Settings(ConfigParser):
    def __init__(self):
        super().__init__()
        self.settings_file = "settings.ini"
        self.read(self.settings_file)

        # If no settings file, create one
        if "TMDB" not in self:
            self["TMDB"] = {"api_key": ""}
            self.save()

    def save(self):
        with open(self.settings_file, "w") as settings_file:
            self.write(settings_file)
