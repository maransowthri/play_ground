from datetime import datetime

import time


def get_time(time_now=datetime.now()):
    print('Current time', time_now)


get_time()
time.sleep(5)
get_time()