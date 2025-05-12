from datetime import datetime
import pytz

class TimeHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TimeHandler, cls).__new__(cls)
            cls._instance._timezone = pytz.timezone('US/Eastern')  # Default
        return cls._instance

    def set_timezone(self, timezone_str):
        try:
            cls._timezone = pytz.timezone(timezone_str)
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