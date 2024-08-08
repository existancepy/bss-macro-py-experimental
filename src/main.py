
from pynput import keyboard
import multiprocessing
import ctypes
import typing
import threading
import eel
import time
import sys

def macro(status, log):
    import modules.macro
    macro = modules.macro.macro(status, log)
    macro.start()
    while True:
        pass
        

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
    import modules.screen.screenData as screenData
    macroProc: typing.Optional[multiprocessing.Process] = None
    #set screen data
    screenData.setScreenData()
    #value to control if macro main loop is running
    #0: stop (terminate process)
    #1: start (start process)
    #2: already running (do nothing)
    #3: already stopped (do nothing)
    run = multiprocessing.Value('i', 3)
    status = multiprocessing.Value(ctypes.c_wchar_p, "")
    log = multiprocessing.Value(ctypes.c_wchar_p, "")
    watch_for_hotkeys(run)

    #setup and launch gui
    gui.run = run
    gui.launch()
    #use run.value to control the macro loop
    while True:
        eel.sleep(0.1)
        if run.value == 1:
            macroProc = multiprocessing.Process(target=macro, args=(status, log))
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
        
        if status == "yes":
            print("hi")
            
            
            
