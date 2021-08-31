import os

import psutil as psutil


# def get_disk_usage(disk):
#     if not os.path.exists(disk):
#         return None
#     statistic = psutil.disk_usage(disk)
#     total = statistic.total
#     used = statistic.used
#     free = statistic.free
#     used_percent = statistic.percent
#
#     return total, used, free, used_percent
#
# def write_error_in_data(data, error):
#
#    file = open("/root/cancelled_data.txt","a")
#    file.write(f'{data} ERROR {error}')
#    file.write("\n")
#    file.close()
#
# def write_finish_data(data, files):
#     file = open("/root/finished_data.txt", "a")
#     file.write(f'{data} FILES {files}')
#     file.write("\n")
#     file.close()