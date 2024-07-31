from datetime import datetime, time

def is_within_working_hours():
    now = datetime.now().time()
    start_time = time(9, 0)  # 09:00 AM
    end_time = time(23, 0)   # 11:00 PM
    return start_time <= now <= end_time
