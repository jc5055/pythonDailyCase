#!/usr/bin/python
#hzjiangcong5055

import  time
import  datetime


timeTemp = time.strftime("%Y%m%d", time.localtime())

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

print(today)
print(yesterday)