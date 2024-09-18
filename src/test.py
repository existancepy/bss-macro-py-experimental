import time
def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration

    while now < end:
        now = get_now()

t = time.process_time()
#do some stuff
sleep(1)
elapsed_time = time.process_time() - t
print(elapsed_time)

t = time.process_time()
#do some stuff
d = 0
while d < 1:
    start = time.perf_counter()
    d += time.perf_counter() - start
elapsed_time = time.process_time() - t
print(elapsed_time)