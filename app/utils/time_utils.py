from datetime import datetime

import pytz


def get_current_time():
    timezone = pytz.timezone('Europe/Moscow')
    current_time = datetime.now(timezone)
    return current_time.replace(microsecond=0).isoformat()
