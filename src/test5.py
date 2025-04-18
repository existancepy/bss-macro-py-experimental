from modules.submacros.hourlyReport import BuffDetector
import time
time.sleep(2)
hourBuffs = {
    "tabby_love": ["top", True, True],
    "polar_power": ["top", True, True],
    "wealth_clock": ["top", True, True],
    "blessing": ["middle", True, True],
    "bloat": ["top", True, True],
}

buff = {
    "blue_boost": ["middle", True, True],
    # "baby_love": ["middle", True, True],
}

bd = BuffDetector(True, "retina")
print(bd.getBuffsWithImage(buff, True))