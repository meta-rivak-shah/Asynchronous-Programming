from pytz import timezone, all_timezones, utc
from datetime import datetime, date, timedelta


def utc_time():
    return utc.localize(datetime.utcnow())