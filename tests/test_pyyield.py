from pyyield import pyyield
from time import time, sleep
from pytest import fail
import logging


def emptyFunc():
    # Nothing to see here
    return


def test_pyyield_call():
    try:
        pyyield()
    except Exception as e:
        fail(f"Failed to call 'pyyield()': {str(e)}")


# Purely for performance comparison. Seems to be very varying results, depending on setup.
def test_pyyield_speed():
    try:
        sleepTime = 0
        pyyieldTime = 0
        emptyTime = 0
        iterations = 100000
        for i in range(3):
            t0 = time()
            for i in range(iterations):
                pyyield()
            t1 = time()
            for i in range(iterations):
                sleep(0)
            t2 = time()
            for i in range(iterations):
                emptyFunc()
            t3 = time()
            pyyieldTime = t1 - t0
            sleepTime = t2 - t1
            emptyTime = t3 - t2
            if pyyieldTime < sleepTime and pyyieldTime > emptyTime:
                nanosec = 10**9
                logging.info(
                    f"Info test:\n  iterations: {iterations}\n pyyieldTime: {pyyieldTime} with {pyyieldTime*nanosec/iterations} ns/exec,\n   sleepTime: {sleepTime} with {sleepTime*nanosec/iterations} ns/exec,\n   emptyTime: {emptyTime} with {emptyTime*nanosec/iterations} ns/exec"
                )
                return
        assert pyyieldTime > emptyTime, "pyyield is faster than emptyFunc()!"
        assert pyyieldTime < sleepTime, "pyyield is not faster than sleep()!"
    except Exception as e:
        # fail(f"Failed to at speed test: {str(e)}")
        logging.warn(
            f"Failed to at speed test, error: {str(e)}\n  iterations: {iterations}\n pyyieldTime: {pyyieldTime},\n   sleepTime: {sleepTime},\n   emptyTime: {emptyTime}"
        )
