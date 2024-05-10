import pyautogui as pag
import time

time.sleep(3)

for i in range(4,6):
    for j in range(1,4):
        content = f'''"cycle_{i}_planter_{j}":cycle_{i}_planter_{j}.get().lower(),\n"cycle_{i}_field_{j}":cycle_{i}_field_{j}.get().lower(),'''
        pag.write(content)
