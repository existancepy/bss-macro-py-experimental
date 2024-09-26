
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
from modules.misc import messageBox

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
def macro(status, log, haste, updateGUI):
    import modules.misc.settingsManager as settingsManager
    import modules.macro as macroModule
    macro = macroModule.macro(status, log, haste, updateGUI)
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
    
    setdat = macro.setdat
    if "share" in setdat["private_server_link"] and setdat["rejoin_method"] == "deeplink":
                messageBox.msgBox(text="You entered a 'share?code' link!\n\nTo fix this:\n1. Paste the link in your browser\n2. Wait for roblox to load in\n3. Copy the link from the top of your browser.  It should now be a 'privateServerLinkCode' link", title='Unsupported private server link')
                return
    macro.start()
    #macro.useItemInInventory("blueclayplanter")
    #function to run a task
    #makes it easy to do any checks after a task is complete (like stinger hunt, rejoin every, etc)
    def runTask(func = None, args = (), resetAfter = True, convertAfter = True):
        #execute the task
        returnVal = None
        if not func is None: returnVal = func(*args)
        #task done
        if resetAfter: macro.reset(convert=convertAfter)

        #do priority tasks
        if macro.night and setdat["stinger_hunt"]:
            macro.stingerHunt()
        if setdat["mondo_buff"]:
            macro.collectMondoBuff()
        if setdat["rejoin_every"]:
            if macro.hasRespawned("rejoin_every", setdat["rejoin_every"]*60*60):
                macro.rejoin("Rejoining (Scheduled)")
                macro.saveTiming("rejoin_every")
        status.value = ""
        return returnVal

    #macro.rejoin()
    while True:
        setdat = macro.setdat
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
        #blender
        if setdat["blender_enable"]:
            with open("./data/user/blender.txt", "r") as f:
                blenderData = ast.literal_eval(f.read())
            f.close()
            #collectTime: time where the blender is done crafting
            #item: the next item number to craft
            #check if its time to collect the previous item
            if blenderData["collectTime"] > -1 and time.time() > blenderData["collectTime"]:
                runTask(macro.blender, args=(blenderData,))
        #planters
        def goToNextCycle(cycle):
            #go to the next cycle
            for _ in range(6):
                cycle += 1
                if cycle > 5:
                    cycle = 1
                for i in range(3): #make sure the cycle is occupied
                    if setdat[f"cycle{cycle}_{i+1}_planter"] != "none" and setdat[f"cycle{cycle}_{i+1}_field"] != "none":
                        return cycle
            else: 
                return False
        planterDataRaw = None
        if setdat["planters_mode"] == 1:
            with open("./data/user/manualplanters.txt", "r") as f:
                planterDataRaw = f.read()
            f.close()
            cycle = goToNextCycle(0)
            #Ensure that there is at least 1 valid slot
            if not planterDataRaw and cycle: #check if planter data exists
                #place planters in cycle
                runTask(macro.placePlanterCycle, args = (cycle,),resetAfter=False)
            elif cycle: #planter data does exist, check if its time to collect them
                planterData = ast.literal_eval(planterDataRaw)
                cycle = planterData["cycle"]
                if time.time() > planterData["harvestTime"]:
                    #Collect planters
                    for i in range(len(planterData["planters"])):
                        runTask(macro.collectPlanter, args=(planterData["planters"][i], planterData["fields"][i]))
                    settingsManager.clearFile("./data/user/manualplanters.txt")
                    #go to the next cycle
                    cycle = goToNextCycle(cycle)
                    #place them
                    runTask(macro.placePlanterCycle, args = (cycle,),resetAfter=False) 
        #mob runs
        for mob, fields in regularMobData.items():
            if not setdat[mob]: continue
            for f in fields:
                if macro.hasMobRespawned(mob, f):
                    runTask(macro.killMob, args=(mob, f,), convertAfter=False)
        #ant challenge
        if setdat["ant_challenge"]: 
            runTask(macro.antChallenge)

        #coconut crab
        if setdat["coconut_crab"] and macro.hasRespawned("coconut_crab", 36*60*60, applyMobRespawnBonus=True):
            macro.coconutCrab()
            
        #stump snail
        if setdat["stump_snail"] and macro.hasRespawned("stump_snail", 96*60*60, applyMobRespawnBonus=True):
            runTask(macro.stumpSnail)
        
        #sticker stack
        if setdat["sticker_stack"]:
            with open("./data/user/sticker_stack.txt", "r") as f:
                stickerStackCD = int(f.read())
            f.close()
            if macro.hasRespawned("sticker_stack", stickerStackCD):
                runTask(macro.collect, args=("sticker_stack",))
        #field boosters
        boostedGatherFields = []
        for k, _ in macroModule.fieldBoosterData.items():
            #check if the cooldown is up
            if setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]) and macro.hasRespawned("last_booster", setdat["boost_seperate"]*60):
                boostedField = runTask(macro.collect, args=(k,))
                if setdat["gather_boosted"] and boostedField:
                    boostedGatherFields.append(boostedField)
        #gather in boosted fields
        #gather for the entire 15min duration
        for field in boostedGatherFields:
            st = time.time()
            while time.time() - st < 15*60:
                runTask(macro.gather, args=(field,), resetAfter=False)

        #add gather tab fields
        gatherFields = []
        for i in range(3):
            if setdat["fields_enabled"][i]:
                gatherFields.append(setdat["fields"][i])
        
        #add planter gather fields
        planterGatherFields = ast.literal_eval(planterDataRaw)["gatherFields"] if planterDataRaw else []
        gatherFields.extend([x for x in planterGatherFields if x not in gatherFields])

        #remove fields that are already in boosted fields
        gatherFields = [x for x in gatherFields if not x in boostedGatherFields]
        
        for field in gatherFields:
            runTask(macro.gather, args=(field,), resetAfter=False)
        print("cycle done")

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
    import modules.misc.appManager as appManager
    import modules.misc.settingsManager as settingsManager
    from modules.discord_bot.discordBot import discordBot
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
    updateGUI = multiprocessing.Value('i', 0)
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
        if discordBotProc.is_alive(): discordBotProc.kill()
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
                messageBox.msgBox(text = f"Your current color profile is {colorProfile}.The required one is sRGB IEC61966-2.1.\
                \nThis is necessary for the macro to work\
                \nTVisit step 6 of the macro installation guide in the discord for instructions", title="Wrong Color Profile")
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
            macroProc = multiprocessing.Process(target=macro, args=(status, log, haste, updateGUI))
            macroProc.start()
            #disconnect detection
            disconnectThread = Thread(target=disconnectCheck, args=(run, status, screenInfo["display_type"]))
            disconnectThread.daemon = True
            disconnectThread.start()
            #haste compensation
            if setdat["haste_compensation"]:
                hasteCompThread = Thread(target=hasteCompensationThread, args=(setdat["movespeed"],haste,))
                hasteCompThread.daemon = True
                hasteCompThread.start()
            #discord bot
            discordBotProc = multiprocessing.Process(target=discordBot, args=(setdat["discord_bot_token"], run, status))
            if setdat["discord_bot"]:
                discordBotProc.start()
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
            macroProc = multiprocessing.Process(target=macro, args=(status, log, haste, updateGUI))
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
        
        #detect if the gui needs to be updated
        if updateGUI.value:
            gui.updateGUI()
            updateGUI.value = 0
    
            
            
            
