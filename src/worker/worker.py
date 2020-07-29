#!/usr/bin/env python3
import sys
import logging
from redis import Redis
from rq import Connection
from util.redis_killer import KillWorker
from util.job_methods import sleep_and_count

def work():

    logging.debug("Initialized Logger")
    logging.Formatter(fmt=None, datefmt=None, style='{')

    with Connection(Redis('redis', 6379)):
        qs = sys.argv[1:] or ['JOB']
        w = KillWorker(qs)
        w.work()

if __name__ == '__main__':
    work()
