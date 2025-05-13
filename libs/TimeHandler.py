from datetime import datetime
import configparser
import pytz
import re


def read_timezone_from_cfg(path="./files/rootthebox.cfg"):
    pattern = r'^\s*time_zone\s*=\s*(".*?")'
    with open(path, 'r') as file:
        for line in file:
            match = re.search(pattern, line.strip())
            if match:
                return match.group(1).strip('"')
    return "UTC"    # Default return


class TimeHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimeHandler, cls).__new__(cls)
            cls._instance._timezone = pytz.timezone(read_timezone_from_cfg())
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

    def get_datetime_object(self):
        now_utc = datetime.utcnow()
        now_utc = pytz.utc.localize(now_utc)
        now_local = now_utc.astimezone(self._timezone)
        return now_local.replace(tzinfo=None)

    def get_iso_time(self, time):
        now_local = datetime.now(self._timezone)
        now_formatted = now_local.strptime(time, "%Y-%m-%dT%H:%M")
        return now_formatted

    def get_current_time(self):
        return str(datetime.now(self._timezone)).split(" ")[1].split(".")[0]

    def refresh_timezone(self):
        self.set_timezone(read_timezone_from_cfg())
        return None
