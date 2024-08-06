
from pynput import keyboard
import multiprocessing
import ctypes
import typing
import threading
import eel
import time

def macro():
    while True:
        print("a")
        time.sleep(1)

def watch_for_hotkeys(run):
    def on_press(key):
        nonlocal run
        if key == keyboard.Key.f1:
            if run.value == 2: return #already running
            run.value = 1
        elif key == keyboard.Key.f3:
            if run.value == 3: return #already stopped
            run.value = 0

    keyboard.Listener(on_press=on_press).start()

if __name__ == "__main__":
    import gui

    macroProc: typing.Optional[multiprocessing.Process] = None

    #value to control if macro main loop is running
    #0: stop (terminate process)
    #1: start (start process)
    #2: already running (do nothing)
    #3: already stopped (do nothing)
    #4: rejoin (stop and trigger rejoin sequence)
    run = multiprocessing.Value('i', 3)
    watch_for_hotkeys(run)

    #setup and launch gui
    gui.run = run
    gui.launch()
    #use run.value to control the macro loop
    while True:
        eel.sleep(0.1)
        if run.value == 1:
            macroProc = multiprocessing.Process(target=macro)
            macroProc.start()
            print("start")
            run.value = 2
            gui.toggleStartStop()
        elif run.value == 0:
            if macroProc:
                print("stop")
                macroProc.kill()
                run.value = 3
                gui.toggleStartStop()
            
            
            
