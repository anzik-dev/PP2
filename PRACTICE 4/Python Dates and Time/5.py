from datetime import datetime
from zoneinfo import ZoneInfo


dt_almaty = datetime.now(ZoneInfo("Asia/Almaty"))
print(dt_almaty)


dt_london = datetime.now(ZoneInfo("Europe/London"))
print(dt_london)