
from pynput import keyboard
import multiprocessing
import ctypes
import typing
from threading import Thread
import eel
import time
import sys
import ast
from discord_webhook import DiscordWebhook

#controller for the macro
def macro(status, log):
    import modules.macro
    macro = modules.macro.macro(status, log)
    macro.start()
    setdat = macro.setdat
    #macro.rejoin()
    while True:
        #gather
        for i in range(3):
            if setdat["fields_enabled"][i]:
                macro.gather(setdat["fields"][i])
        

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
    import modules.controls.keyboard
    import modules.logging.log as logModule
    import modules.controls.mouse as mouse
    import modules.misc.settingsManager as settingsManager
    keyboardModule = modules.controls.keyboard.keyboard(0)
    macroProc: typing.Optional[multiprocessing.Process] = None
    #set screen data
    screenData.setScreenData()
    #value to control if macro main loop is running
    #0: stop (terminate process)
    #1: start (start process)
    #2: already running (do nothing)
    #3: already stopped (do nothing)
    manager = multiprocessing.Manager()
    run = multiprocessing.Value('i', 3)
    status = manager.Value(ctypes.c_wchar_p, "none")
    log = manager.Value(ctypes.c_wchar_p, "")
    prevLog = ""
    watch_for_hotkeys(run)
    logger = logModule.log(log, False, None)

    #setup and launch gui
    gui.run = run
    gui.launch()
    #use run.value to control the macro loop
    while True:
        eel.sleep(0.1)
        if run.value == 1:
            #create and set webhook obj for the logger
            setdat = settingsManager.loadAllSettings()
            logger.enableWebhook = setdat["enable_webhook"]
            logger.webhookURL = setdat["webhook_link"]

            macroProc = multiprocessing.Process(target=macro, args=(status, log))
            macroProc.start()
            logger.webhook("Macro Started", "exih macro", "purple")
            run.value = 2
            gui.toggleStartStop()
        elif run.value == 0:
            if macroProc:
                logger.webhook("Macro Stopped", "exih macro", "red")
                macroProc.kill()
                run.value = 3
                gui.toggleStartStop()
                keyboardModule.releaseMovement()
                mouse.mouseUp()

        #detect a new log message
        if log.value != prevLog:
            #get the logData and format the message based on its type
            logData = ast.literal_eval(log.value)
            if logData["type"] == "webhook": #webhook
                msg = f"{logData['title']}<br>{logData['desc']}"

            #add it to gui
            gui.log(logData["time"], msg, logData["color"])
            prevLog = log.value
    
            
            
            
