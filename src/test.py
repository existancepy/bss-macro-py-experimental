import time
import pyautogui as pag
from pynput.keyboard import Key, Controller

keyboard = Controller()

def high_precision_sleep(duration):
    start_time = time.perf_counter()
    while True:
        elapsed_time = time.perf_counter() - start_time
        remaining_time = duration - elapsed_time
        if remaining_time <= 0:
            break
        if remaining_time > 0.02:  # Sleep for 5ms if remaining time is greater
            time.sleep(max(remaining_time/2, 0.0001))  # Sleep for the remaining time or minimum sleep interval
        else:
            pass

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

def keyDown(k, pause = True):
    keyboard.press(k)
   #pag.keyDown(k, _pause = pause)

def keyUp(k, pause = True):
    keyboard.release(k)
   #pag.keyUp(k, _pause = pause)

t = 0.6
k = "a"

script_start_time = time.perf_counter()
time.sleep(t)
time_now = time.perf_counter()
elapsed_time = (time_now - script_start_time)
print("[%.6f] time.sleep" % elapsed_time)


script_start_time = time.perf_counter()
keyDown(k, False)
for _ in range(round(t/0.1)):
    high_precision_sleep(0.1)
keyUp(k, False)
time_now = time.perf_counter()
elapsed_time = (time_now - script_start_time)
print("[%.6f] high_precision_sleep" % elapsed_time)


script_start_time = time.perf_counter()
keyDown(k, False)
for _ in range(round(t/0.1)):
    sleep(0.1)
keyUp(k, False)
time_now = time.perf_counter()
elapsed_time = (time_now - script_start_time)
print("[%.6f] sleep" % elapsed_time)