
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
from datetime import datetime

#controller for the macro
def macro(status, log):
    import modules.macro as macroModule
    macro = macroModule.macro(status, log)
    macro.start()
    setdat = macro.setdat
    #function to run a task
    #makes it easy to do any checks after a task is complete (like stinger hunt, rejoin every, etc)
    def runTask(func = None, args = (), resetAfter = True, convertAfter = True):
        #execute the task
        if not func is None: func(*args)
        #task done
        if resetAfter: macro.reset(convert=convertAfter)

        #do priority tasks
        if setdat["mondo_buff"]:
            macro.collectMondoBuff()

    #macro.rejoin()
    while True:
        #run empty task
        #this is in case no other settings are selected 
        runTask(resetAfter=False)
        #collect
        for k, _ in macroModule.collectData.items():
            if setdat[k]:
                #check if the cooldown is up
                if macro.hasRespawned(k, macro.collectCooldowns[k]):
                    runTask(macro.collect, args=(k,))
        #ant challenge
        if setdat["ant_challenge"]: 
            runTask(macro.antChallenge)
        #gather
        for i in range(3):
            if setdat["fields_enabled"][i]:
                runTask(macro.gather, args=(setdat["fields"][i],), resetAfter=False)

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

    #check color profile
    if sys.platform == "darwin":
        try:
            cmd = """
                osascript -e 'tell application "Image Events" to display profile of display 1' 
                """
            colorProfile = subprocess.check_output(cmd, shell=True).decode(sys.stdout.encoding)
            colorProfile = colorProfile.strip()
            if colorProfile == "missing value": colorProfile = "Color LCD"
            if not "sRGB IEC61966" in colorProfile:
                pag.alert(text = f'Your current color profile is {colorProfile}.The recommended one is sRGB IEC61966-2.1.\
                \n(This is optional, but some features like backpack detection wont work)\
                \nTVisit step 6 of the macro installation guide in the discord for instructions"')
        except:
            pass
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
    
            
            
            
