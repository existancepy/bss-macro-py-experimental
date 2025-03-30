import time
from modules.submacros.hasteCompensation import HasteCompensation
import random
hasteCompensation = HasteCompensation(True, 28)


def getHaste():
    st = time.perf_counter()
    haste = random.randint(28, 28)
    return st, time.perf_counter(), haste

def walk(duration):
    base_speed = 28
    target_distance = base_speed * duration  # Total distance the player should travel
    traveled_distance = 0  # Tracks total integrated distance

    start_time = time.perf_counter()
    prev_time = start_time
    _, _, prev_speed = getHaste()  # Get initial speed

    while traveled_distance < target_distance:
        # Get new speed and current timestamp
        current_time = time.perf_counter()
        _, _, current_speed = getHaste()

        # Compute time difference (delta_t)
        delta_t = current_time - prev_time

        # Apply trapezoidal integration to calculate traveled distance
        traveled_distance += ((prev_speed + current_speed) / 2) * delta_t

        # Update previous values
        prev_time = current_time
        prev_speed = current_speed

    elapsed_time = time.perf_counter() - start_time
    print(f"Walking complete. Traveled distance: {traveled_distance:.2f} units in {elapsed_time:.2f} seconds.")

walk(0.1)