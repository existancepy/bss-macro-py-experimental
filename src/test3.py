import time
from modules.submacros.hasteCompensation import HasteCompensation
import random
hasteCompensation = HasteCompensation(True, 28)


def getHaste():
    st = time.perf_counter()
    haste = random.randint(28, 28)
    return st, time.perf_counter(), haste

baseSpeed = 28
duration = 3
targetDistance = baseSpeed * duration  # Total distance the player should travel
traveledDistance = 0  # Tracks total integrated distance
startTime = time.perf_counter()
prevTime = startTime

while traveledDistance < targetDistance:
    currentTime = time.perf_counter()
    deltaT = deltaT = max(currentTime - prevTime, 1e-6)
    speed = max(random.randint(28, 28), 28)
    traveledDistance += speed * deltaT

    prevTime = currentTime
    time.sleep(0.01)

elapsed_time = time.perf_counter() - startTime
print(f"current speed: {speed}, original time: {duration}, actual travel time: {elapsed_time}")
