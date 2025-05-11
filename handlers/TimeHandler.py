from datetime import datetime
import pytz

class TimeHandler:
    _timezone = pytz.timezone('UTC')  # Class-level default

    @classmethod
    def set_timezone(cls, timezone_str):
        try:
            cls._timezone = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            print(f"Unknown timezone: {timezone_str}")

    @classmethod
    def get_timezone(cls):
        return cls._timezone.zone

    @classmethod
    def get_datetime(cls):
        return datetime.now(cls._timezone)

    @classmethod
    def get_iso_time(cls):
        return datetime.now(cls._timezone).strftime("%Y-%m-%dT%H:%M")

    @classmethod
    def get_current_time(cls):
        return str(datetime.now(cls._timezone)).split(" ")[1].split(".")[0]