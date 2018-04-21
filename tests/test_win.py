import sys
import os
import time
import signal
import subprocess as sp
import pytest


if sys.platform != 'win32':
    pytest.skip("These tests are for Windows compatibility.",
                allow_module_level=True)


def test_sig():
    """Basic SIGTERM"""
    proc = sp.Popen(
        'python tests/fake_main.py'.split(),
        stdout=sp.PIPE,
        stderr=sp.STDOUT,
        creationflags=sp.CREATE_NEW_PROCESS_GROUP
    )
    time.sleep(0.1)
    # proc.send_signal(signal.CTRL_BREAK_EVENT)
    # os.kill(proc.pid, signal.CTRL_C_EVENT)
    os.kill(proc.pid, signal.CTRL_BREAK_EVENT)
    print('Send signal')
    proc.wait(timeout=5)
    assert proc.returncode == 0

    expected = [
        'Running forever',
        'Received signal: SIGBREAK',
        'Entering shutdown phase',
        'pending tasks till complete',
        'Closing the loop',
        'Bye!',
    ]

    stdout = proc.stdout.read().decode()
    print(stdout)
    assert all(phrase in stdout for phrase in expected)
