from datetime import datetime

def time_difference_in_days(datetime1_str, datetime2_str):

    format_str = "%Y-%m-%d UTC%z"
    

    datetime1 = datetime.strptime(datetime1_str, format_str)
    datetime2 = datetime.strptime(datetime2_str, format_str)
    

    delta = abs(datetime1 - datetime2)
    

    return delta.days


datetime1_str = input()
datetime2_str = input()


result = time_difference_in_days(datetime1_str, datetime2_str)

print(result)