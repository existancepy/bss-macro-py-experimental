from modules.controls.sleep import sleep
import time

t = time.process_time()
sleep(3)
elapsed_time = time.process_time() - t
print(elapsed_time)

d = 3
i = 0
t = time.process_time()
while i < d:
    i += 0.1
    sleep(0.1)
elapsed_time = time.process_time() - t
print(elapsed_time)