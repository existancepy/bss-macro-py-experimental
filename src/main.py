
from pynput import keyboard
import multiprocessing
import ctypes
import typing
from threading import Thread
import eel
import time
import sys
import ast
import subprocess

def hasteCompensationThread(baseSpeed, haste):
    from modules.submacros.hasteCompensation import hasteCompensation
    global stopThreads
    while not stopThreads:
        hasteCompensation(baseSpeed, haste)

def disconnectCheck(run, status, display_type):
    from modules.misc.imageManipulation import adjustImage
    from modules.screen.imageSearch import locateImageOnScreen
    import pyautogui as pag
    mw, mh = pag.size()
    img = adjustImage("./images/menu", "disconnect", display_type)
    while not stopThreads:
        if locateImageOnScreen(img, mw/3, mh/2.8, mw/2.3, mh/5, 0.7):
            print("disconnected")
            run.value = 4

#controller for the macro
def macro(status, log, haste):
    import modules.macro as macroModule
    macro = macroModule.macro(status, log, haste)
    #invert the regularMobsInFields dict
    #instead of storing mobs in field, store the fields associated with each mob
    regularMobData = {}
    for k,v in macroModule.regularMobInFields.items():
        for x in v:
            if x in regularMobData:
                regularMobData[x].append(k)
            else:
                regularMobData[x] = [k]
    #Limit werewolf to just pumpkin 
    regularMobData["werewolf"] = ["pumpkin"]
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
        if macro.night and setdat["stinger_hunt"]:
            macro.stingerHunt()
        if setdat["mondo_buff"]:
            macro.collectMondoBuff()
        if setdat["rejoin_every"]:
            if macro.hasRespawned("rejoin_every", setdat["rejoin_every"]):
                macro.rejoin("Rejoining (Scheduled)")
                macro.saveTiming("rejoin_every")
        status.value = ""

    #macro.rejoin()
    while True:
        #run empty task
        #this is in case no other settings are selected 
        runTask(resetAfter=False)
        #collect
        for k, _ in macroModule.collectData.items():
            #check if the cooldown is up
            if setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]):
                runTask(macro.collect, args=(k,))

        if setdat["sticker_printer"] and macro.hasRespawned("sticker_printer", macro.collectCooldowns["sticker_printer"]):
            runTask(macro.collectStickerPrinter)
        
        #mob runs
        for mob, fields in regularMobData.items():
            if not setdat[mob]: continue
            for f in fields:
                if macro.hasMobRespawned(mob, f):
                    runTask(macro.killMob, args=(mob, f,), convertAfter=False)
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
    print("Loading gui...")
    global stopThreads
    import gui
    import modules.screen.screenData as screenData
    from modules.controls.keyboard import keyboard as keyboardModule
    import modules.logging.log as logModule
    import modules.controls.mouse as mouse
    import modules.misc.settingsManager as settingsManager
    import modules.misc.appManager as appManager
    macroProc: typing.Optional[multiprocessing.Process] = None
    #set screen data
    screenData.setScreenData()
    screenInfo = screenData.getScreenData()
    #value to control if macro main loop is running
    #0: stop (terminate process)
    #1: start (start process)
    #2: already running (do nothing)
    #3: already stopped (do nothing)
    manager = multiprocessing.Manager()
    run = multiprocessing.Value('i', 3)
    status = manager.Value(ctypes.c_wchar_p, "none")
    log = manager.Value(ctypes.c_wchar_p, "")
    haste = multiprocessing.Value('d', 0)
    prevLog = ""
    watch_for_hotkeys(run)
    logger = logModule.log(log, False, None)

    def stopApp(page= None, sockets = None):
        global stopThreads
        stopThreads = True
        print("stop")
        #print(sockets)
        macroProc.kill()
        keyboardModule.releaseMovement()
        mouse.mouseUp()
        
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
        eel.sleep(0.2)
        if run.value == 1:
            #create and set webhook obj for the logger
            setdat = settingsManager.loadAllSettings()
            logger.enableWebhook = setdat["enable_webhook"]
            logger.webhookURL = setdat["webhook_link"]
            haste.value = setdat["movespeed"]
            stopThreads = False
            macroProc = multiprocessing.Process(target=macro, args=(status, log, haste))
            macroProc.start()
            #disconnect detection
            disconnectThread = Thread(target=disconnectCheck, args=(run, status, screenInfo["display_type"]))
            disconnectThread.daemon = True
            disconnectThread.start()
            if setdat["haste_compensation"]:
                hasteCompThread = Thread(target=hasteCompensationThread, args=(setdat["movespeed"],haste,))
                hasteCompThread.daemon = True
                hasteCompThread.start()
            logger.webhook("Macro Started", f'Existance Macro v2.0\nDisplay: {screenInfo["display_type"]}, {screenInfo["screen_width"]}x{screenInfo["screen_height"]}', "purple")
            run.value = 2
            gui.toggleStartStop()
        elif run.value == 0:
            if macroProc:
                logger.webhook("Macro Stopped", "exih macro", "red")
                run.value = 3
                gui.toggleStartStop()
                stopApp()
                disconnectThread.join()
        elif run.value == 4: #disconnected
            macroProc.kill()
            logger.webhook("","Disconnected", "red", "screen")
            appManager.closeApp("Roblox")
            keyboardModule.releaseMovement()
            mouse.mouseUp()
            macroProc = multiprocessing.Process(target=macro, args=(status, log, haste))
            macroProc.start()
            run.value = 2

        #detect a new log message
        if log.value != prevLog:
            #get the logData and format the message based on its type
            logData = ast.literal_eval(log.value)
            if logData["type"] == "webhook": #webhook
                msg = f"{logData['title']}<br>{logData['desc']}"

            #add it to gui
            gui.log(logData["time"], msg, logData["color"])
            prevLog = log.value
    
            
            
            
