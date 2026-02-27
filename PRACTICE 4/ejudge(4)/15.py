import math
from datetime import datetime, timedelta


def get_utc_time(line):
    parts = line.split() # ['2000-05-10', 'UTC+02:30']
    dt = datetime.strptime(parts[0], "%Y-%m-%d")
    
  
    tz = parts[1][3:] 
    sign = 1 if tz[0] == '+' else -1
    h, m = map(int, tz[1:].split(':'))
   
    offset = timedelta(hours=h, minutes=m)
    return dt - offset if sign == 1 else dt + offset


line_birth = input()
line_now = input()


birth_dt = datetime.strptime(line_birth.split()[0], "%Y-%m-%d")
b_month, b_day = birth_dt.month, birth_dt.day


now_utc = get_utc_time(line_now)


current_year = datetime.strptime(line_now.split()[0], "%Y-%m-%d").year

for year in [current_year, current_year + 1]:
    try:

        bday_local = datetime(year, b_month, b_day)
    except ValueError:
        bday_local = datetime(year, 2, 28)
    
 
    tz_b = line_birth.split()[1][3:]
    sign_b = 1 if tz_b[0] == '+' else -1
    hb, mb = map(int, tz_b[1:].split(':'))
    bday_utc = bday_local - timedelta(hours=hb, minutes=mb) if sign_b == 1 else bday_local + timedelta(hours=hb, minutes=mb)


    diff = (bday_utc - now_utc).total_seconds()
    
    if diff >= 0:
  
        print(math.ceil(diff / 86400))
        break