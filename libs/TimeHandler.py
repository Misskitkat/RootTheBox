from datetime import datetime
import configparser
import pytz


def read_timezone_from_cfg(path="files/rootthebox.cfg"):
    config = configparser.ConfigParser()
    config.read(path)

    try:
        tz = config.get('general', 'time_zone').strip('"').strip("'")
        return pytz.timezone(tz)
    except (configparser.NoSectionError, configparser.NoOptionError, pytz.UnknownTimeZoneError) as e:
        print(f"Error reading timezone: {e}")
        return pytz.timezone("UTC")


class TimeHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimeHandler, cls).__new__(cls)
            cls._instance._timezone = read_timezone_from_cfg() # Default
        return cls._instance

    def set_timezone(self, timezone_str):
        try:
            self._timezone = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            print(f"Unknown timezone: {timezone_str}")

    def get_timezone(self):
        return self._timezone.zone

    def get_datetime(self):
        return datetime.now(self._timezone)

    def get_iso_time(self):
        return datetime.now(self._timezone).strftime("%Y-%m-%dT%H:%M")

    def get_current_time(self):
        return str(datetime.now(self._timezone)).split(" ")[1].split(".")[0]