import time
import datetime

# 时间格式化
# https://blog.csdn.net/wteruiycbqqvwt/article/details/115706505
def format_dt(string):
    time_format = datetime.datetime.strptime(string, '%a, %d %b %Y %H:%M:%S')
    time_format = datetime.datetime.strftime(time_format, "%Y-%M-%d %H:%M:%S")
    return time_format