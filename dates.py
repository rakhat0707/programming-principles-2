from datetime import datetime, timedelta

today = datetime.now()
new_date = today - timedelta(days=5)

print("Current date:", today)
print("5 days ago:", new_date)

from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

from datetime import datetime

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("Original:", now)
print("Without microseconds:", without_microseconds)

from datetime import datetime

date1 = datetime(2026, 2, 1, 12, 0, 0)
date2 = datetime(2026, 2, 22, 18, 30, 0)

difference = date2 - date1

print("Difference in seconds:", int(difference.total_seconds()))

