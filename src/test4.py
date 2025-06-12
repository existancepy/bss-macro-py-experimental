import pygetwindow as gw # pip3 install pygetwindow
import time

time.sleep(2)
windows = gw.getAllTitles()
for win in windows:
    geometry = gw.getWindowGeometry(win)
    if "roblox roblox" in win.lower():
        print(f'Window title: {win}')
        print(f'> top-left X coordinate: {geometry[0]}')
        print(f'> top-left Y coordinate: {geometry[1]}')
        print(f'> width: {geometry[2]}')
        print(f'> height: {geometry[3]}\n')