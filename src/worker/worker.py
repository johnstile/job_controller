#!/usr/bin/env python3
import sys
import logging
from redis import Redis
from redis_killer import KillWorker
from somewhere import sleep_and_count_me
from util import job_methods

def work():

    logging.debug("Initialized Logger")
    logging.Formatter(fmt=None, datefmt=None, style='{')

    with Connection(Redis('redis', 6379)):
        qs = sys.argv[1:] or ['default'] or ['JOB']
        w = KillWorker(qs)
        w.work()

if __name__ == '__main__':
    work()
