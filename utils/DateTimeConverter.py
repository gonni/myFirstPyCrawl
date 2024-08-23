import datetime

def getYYYYMMDD(delta_day) -> str:
    now = datetime.datetime.now() + datetime.timedelta(days=delta_day)
    return now.strftime("%Y%m%d")

print(getYYYYMMDD(1))
print(getYYYYMMDD(0))
print(getYYYYMMDD(-1))