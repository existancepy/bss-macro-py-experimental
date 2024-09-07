import time
leftright_start = 500
leftright_end = 19000
cycle_end = 24000

#left-right movement
moves = 14
move_delay = 310
while True:
    start_time = time.time()
    t = time.time()
    for i in range(1,3):
        for j in range(1,moves+1):
            t = time.time()
            print(i* 2*move_delay*moves - 2*move_delay*moves-leftright_start +j* move_delay - (t-start_time)*1000)
            quit()