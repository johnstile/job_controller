#!/usr/bin/env python3

import os
from threading import Thread
import time
import signal

from rq import Worker, Queue
from rq.job import Job

import logging
logging.basicConfig(level=logging.DEBUG)


kill_key = "rq:jobs:kill"
class KillJob(Job):
    """Patch rq.Job, adding Job kill support
    This starts a Thread to monitor Redis key rq:jobs:kill
    If the Job's ID is listed, kill the process
    Default rq can't ended a job once running.
    REF: https://github.com/rq/rq/issues/684
    """

    def kill(self):
        """ Force kills the current job causing it to fail """
        if self.is_started:
            self.connection.sadd(kill_key, self.get_id())

    def _execute(self):
        def check_kill(conn, id, interval=1):
            while True:
                res = conn.srem(kill_key, id)
                if res > 0:
                    logging.debug(f"Received Kill. Pid: {os.getpid()}")
                    os.kill(os.getpid(), signal.SIGKILL)
                time.sleep(interval)

        logging.debug(f"Monitoring: {kill_key} for: {os.getpid()}")
        t = Thread(target=check_kill, args=(self.connection, self.get_id()))
        t.start()
        return super()._execute()


class KillQueue(Queue):
    """Patch rq.Queue, to add Job kill support"""
    job_class = KillJob


class KillWorker(Worker):
    """Patch rq.Worker, to add Job kill support"""
    queue_class = KillQueue
    job_class = KillJob
