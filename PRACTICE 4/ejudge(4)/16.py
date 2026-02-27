from datetime import datetime, timedelta

def get_utc_seconds(line):
 
    parts = line.split()
    date_str = parts[0] + " " + parts[1]
    tz_str = parts[2].replace("UTC", "") 
   
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    

    sign = 1 if tz_str[0] == '+' else -1
    h, m = map(int, tz_str[1:].split(':'))
    

    offset = timedelta(hours=h, minutes=m)
    if sign == 1:
        dt_utc = dt - offset
    else:
        dt_utc = dt + offset
        

    return dt_utc.timestamp()


start_utc = get_utc_seconds(input())
end_utc = get_utc_seconds(input())


print(int(end_utc - start_utc))
