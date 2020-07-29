#!/usr/bin/env python3

import time
def sleep_and_count(now, *args, **kwargs):
    """
    A long running process, communicate status
    :param now: string date
    """
    counter = 100
    while counter > 0:
        counter -= 1
        time.sleep(1)