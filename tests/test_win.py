import sys
import asyncio
import os
import time
import threading
from signal import SIGINT, SIGTERM
import signal
from concurrent.futures import ThreadPoolExecutor
from aiorun import run, shutdown_waits_for, _DO_NOT_CANCEL_COROS
import pytest


def kill(sig=SIGTERM, after=0.01):
    """Tool to send a signal after a pause"""

    def job():
        pid = os.getpid()
        time.sleep(after)
        os.kill(pid, sig)

    t = threading.Thread(target=job)
    t.start()


def newloop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def test_sigterm():
    """Basic SIGTERM"""
    import subprocess as sp
    proc = sp.Popen(
        'python tests/fake_main.py'.split(),
        stdout=sys.stdout,
        stderr=sp.STDOUT,
        creationflags=sp.CREATE_NEW_PROCESS_GROUP
    )
    time.sleep(3.0)
    # proc.send_signal(signal.CTRL_C_EVENT)
    os.kill(proc.pid, signal.CTRL_BREAK_EVENT)
    print('Send signal')
    assert proc.returncode == 0
