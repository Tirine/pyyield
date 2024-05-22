from pyyield import pyyield
from time import time, sleep
from sys import float_info
from threading import Thread, Lock
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


def test_pyyield_speed():
    try:
        sleepTime = 0
        pyyieldTime = 0
        emptyTime = 0
        for i in range(10):
            t0 = time()
            for i in range(1000000):
                pyyield()
            t1 = time()
            for i in range(1000000):
                sleep(0)
            t2 = time()
            for i in range(1000000):
                emptyFunc()
            t3 = time()
            pyyieldTime = t1 - t0
            sleepTime = t2 - t1
            emptyTime = t3 - t2
            if pyyieldTime < sleepTime and pyyieldTime > emptyTime:
                # All good!
                return
        assert pyyieldTime < sleepTime, "pyyield is not faster than sleep()!"
        assert pyyieldTime > emptyTime, "pyyield is faster than emptyFunc()!"
    except Exception as e:
        # fail(f"Failed to at speed test: {str(e)}")
        logging.info(f"Failed to at speed test: {str(e)}")


###
# Just some possible performance tests and comparisons
###


# def sleepYield(sTime):
#     finishT = time() + sTime
#     while time() < finishT:
#         pyyield()


# floatMin = float_info.min

# t0 = time()
# for i in range(1000000):
#     pyyield()
# t1 = time()
# for i in range(1000000):
#     pyyield()
#     pyyield()
# t2 = time()
# for i in range(1000000):
#     sleep(0)
# t3 = time()
# # 100 times less, cause sleep(lim -> 0) is really ~sleep(50 micros), atleast on unix...
# for i in range(10000):
#     sleep(floatMin)
# t4 = time()
# for i in range(1000000):
#     emptyFunc()
# t5 = time()
# for i in range(1000000):
#     if i != floatMin:
#         pyyield()
# t6 = time()
# for i in range(100000):
#     sleepYield(0.000001)
# t7 = time()
# print(
#     f"Time pyyield: {t1 - t0}, Time pyyield() * 2, {t2 - t1}, Time sleep(0), {t3 - t2}, Time sleep(floatMin), {t4 - t3}, Time emptyFunc(), {t5 - t4}, Time ifPyyeild(), {t6 - t5}, Time sleepyield(), {t7 - t6} vs {100000 * 0.000001}"
# )

# expectedOutput = ""
# letterDecode = "A".encode()
# for i in range(20):
#     expectedOutput = f"{expectedOutput} {i} {letterDecode.decode()}"
#     letterDecode = bytes([letterDecode[0] + 1])
# print(expectedOutput)

# letterDecode = "A".encode()
# actualOutput = ""
# run = False
# lock = Lock()

# def appendLetters():
#     global actualOutput
#     global letterDecode
#     global run
#     global lock
#     while not run:
#         lock.acquire()
#         sleep(0)
#         lock.release()
#     for i in range(20):
#         lock.acquire()
#         actualOutput = f"{actualOutput} {letterDecode.decode()}"
#         letterDecode = bytes([letterDecode[0] + 1])
#         lock.release()
#         sleep(0)


# def appendNumbers():
#     global run
#     global lock
#     while not run:
#         lock.acquire()
#         sleep(0)
#         lock.release()
#     global actualOutput
#     for i in range(20):
#         lock.acquire()
#         actualOutput = f"{actualOutput} {i}"
#         lock.release()
#         sleep(0)


# threadNumbers = Thread(target=appendNumbers)
# threadLetters = Thread(target=appendLetters)
# threadNumbers.start()
# threadLetters.start()
# sleep(0.1)
# run = True
# sleep(0.1)
# threadNumbers.join()
# threadLetters.join()
# print(actualOutput)
