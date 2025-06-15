# -*- coding: utf-8 -*-

import datetime


def get_now_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return formatted_time


def is_within_time_range(
    start_time=datetime.time(11, 0), end_time=datetime.time(7, 30)
):
    current_time = datetime.datetime.now().time()

    if start_time <= end_time:
        return start_time <= current_time <= end_time
    else:
        return start_time <= current_time or current_time <= end_time


if __name__ == "__main__":
    print(is_within_time_range(datetime.time(23, 00), datetime.time(7, 30)))
