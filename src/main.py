
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
import copy

def hasteCompensationThread(baseSpeed, isRetina, haste):
    from modules.submacros.hasteCompensation import HasteCompensation
    hasteCompensation = HasteCompensation(isRetina, baseSpeed)
    global stopThreads
    while not stopThreads:
        haste.value = hasteCompensation.getHaste()

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
            time.sleep(300) #5 min cd to let the macro run through all 3 rejoins

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
    
    if "share" in macro.setdat["private_server_link"] and macro.setdat["rejoin_method"] == "deeplink":
                messageBox.msgBox(text="You entered a 'share?code' link!\n\nTo fix this:\n1. Paste the link in your browser\n2. Wait for roblox to load in\n3. Copy the link from the top of your browser.  It should now be a 'privateServerLinkCode' link", title='Unsupported private server link')
                return
    macro.start()
    #macro.useItemInInventory("blueclayplanter")
    #function to run a task
    #makes it easy to do any checks after a task is complete (like stinger hunt, rejoin every, etc)
    def runTask(func = None, args = (), resetAfter = True, convertAfter = True):
        #execute the task
        returnVal = func(*args) if func else None
        #task done
        if resetAfter: 
            macro.reset(convert=convertAfter)

        #do priority tasks
        if macro.night and macro.setdat["stinger_hunt"]:
            macro.stingerHunt()
        if macro.setdat["mondo_buff"]:
            macro.collectMondoBuff()
        if macro.setdat["rejoin_every"]:
            if macro.hasRespawned("rejoin_every", macro.setdat["rejoin_every"]*60*60):
                macro.rejoin("Rejoining (Scheduled)")
                macro.saveTiming("rejoin_every")
        status.value = ""
        return returnVal

    #macro.rejoin()
    while True:
        macro.setdat = settingsManager.loadAllSettings()
        #run empty task
        #this is in case no other settings are selected 
        runTask(resetAfter=False)

        #handle quests
        questGatherFields = []

        if macro.setdat["polar_bear_quest"]:
            questGiver = "polar bear"
            questObjective = macro.findQuest(questGiver)
            if questObjective is None: #quest does not exist
                questObjective = macro.getNewQuest(questGiver, False)
            elif not len(questObjective): #quest completed
                questObjective = macro.getNewQuest(questGiver, True)
                macro.incrementHourlyStat("quests_completed", 1)
            else:
                for obj in questObjective:
                    objData = obj.split("_")
                    if objData[0] == "gather":
                        questGatherFields.append(objData[1])
                    elif objData[0] == "kill":
                        macro.setdat[objData[2]] = True
        if macro.setdat["honey_bee_quest"]:
            questGiver = "honey bee"
            questObjective = macro.findQuest(questGiver)
            if questObjective is None:  # quest does not exist
                questObjective = macro.getNewQuest(questGiver, False)
            elif not len(questObjective):  # quest completed
                questObjective = macro.getNewQuest(questGiver, True)
            else:
                for obj in questObjective:
                    objData = obj.split("_")
                    if objData[0] == "token" and objData[1] == "honeytoken":
                        macro.setdat[objData[0] and objData[1]] = True
                    
        #collect
        for k, _ in macroModule.collectData.items():
            #check if the cooldown is up
            if macro.setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]):
                runTask(macro.collect, args=(k,))

        if macro.setdat["sticker_printer"] and macro.hasRespawned("sticker_printer", macro.collectCooldowns["sticker_printer"]):
            runTask(macro.collectStickerPrinter)
        #blender
        if macro.setdat["blender_enable"]:
            with open("./data/user/blender.txt", "r") as f:
                blenderData = ast.literal_eval(f.read())
            f.close()
            #collectTime: time where the blender is done crafting
            #item: the next item number to craft
            #check if its time to collect the previous item
            if blenderData["collectTime"] > -1 and time.time() > blenderData["collectTime"]:
                runTask(macro.blender, args=(blenderData,))
        #mob runs
        for mob, fields in regularMobData.items():
            if not macro.setdat[mob]: continue
            for f in fields:
                if macro.hasMobRespawned(mob, f):
                    runTask(macro.killMob, args=(mob, f,), convertAfter=False)
        #planters
        def goToNextCycle(cycle):
            #go to the next cycle
            for _ in range(6):
                cycle += 1
                if cycle > 5:
                    cycle = 1
                for i in range(3): #make sure the cycle is occupied
                    if macro.setdat[f"cycle{cycle}_{i+1}_planter"] != "none" and macro.setdat[f"cycle{cycle}_{i+1}_field"] != "none":
                        return cycle
            else: 
                return False
        planterDataRaw = None
        if macro.setdat["planters_mode"] == 1:
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
        #ant challenge
        if macro.setdat["ant_challenge"]: 
            runTask(macro.antChallenge)

        #coconut crab
        if macro.setdat["coconut_crab"] and macro.hasRespawned("coconut_crab", 36*60*60, applyMobRespawnBonus=True):
            macro.coconutCrab()
            
        #stump snail
        if macro.setdat["stump_snail"] and macro.hasRespawned("stump_snail", 96*60*60, applyMobRespawnBonus=True):
            runTask(macro.stumpSnail)
        
        #sticker stack
        if macro.setdat["sticker_stack"]:
            with open("./data/user/sticker_stack.txt", "r") as f:
                stickerStackCD = int(f.read())
            f.close()
            if macro.hasRespawned("sticker_stack", stickerStackCD):
                runTask(macro.collect, args=("sticker_stack",))

        #auto field boost
        if macro.setdat["Auto_Field_Boost"]:
            if macro.hasAFBRespawned("AFB_dice_cd", macro.setdat["AFB_rebuff"]*60) or macro.hasAFBRespawned("AFB_glitter_cd", macro.setdat["AFB_rebuff"]*60-20):
                runTask(macro.AFB)
            else: continue

        #field boosters
        boostedGatherFields = []
        for k, _ in macroModule.fieldBoosterData.items():
            #check if the cooldown is up
            if macro.setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]) and macro.hasRespawned("last_booster", macro.setdat["boost_seperate"]*60):
                boostedField = runTask(macro.collect, args=(k,))
                if macro.setdat["gather_boosted"] and boostedField:
                    boostedGatherFields.append(boostedField)
        #gather in boosted fields
        #gather for the entire 15min duration
        for field in boostedGatherFields:
            st = time.time()
            while time.time() - st < 15*60:
                #auto field boost
                if macro.setdat["Auto_Field_Boost"]:
                    if macro.hasAFBRespawned("AFB_dice_cd", macro.setdat["AFB_rebuff"]*60) or macro.hasAFBRespawned("AFB_glitter_cd", macro.setdat["AFB_rebuff"]*60-20):                        
                        macro.reset()
                        runTask(macro.AFB)
                runTask(macro.gather, args=(field,), resetAfter=False)

        #add gather tab fields
        gatherFields = []
        for i in range(3):
            if macro.setdat["fields_enabled"][i]:
                gatherFields.append(macro.setdat["fields"][i])
        
        #add planter gather fields
        planterGatherFields = ast.literal_eval(planterDataRaw)["gatherFields"] if planterDataRaw else []
        gatherFields.extend([x for x in planterGatherFields if x not in gatherFields])

        #remove fields that are already in boosted fields
        gatherFields = [x for x in gatherFields if not x in boostedGatherFields]
        
        for field in gatherFields:
            runTask(macro.gather, args=(field,), resetAfter=False)

        #do quests
        questGatherFields = [x for x in questGatherFields if not (x in gatherFields or x in boostedGatherFields)]
        print(questGatherFields)
        #setup the override
        questGatherOverrides = {}
        if macro.setdat["quest_gather_mins"]:
            questGatherOverrides["mins"] = macro.setdat["quest_gather_mins"]
        if macro.setdat["quest_gather_return"] != "no override":
            questGatherOverrides["return"] = macro.setdat["quest_gather_return"]
        for field in questGatherFields:
            runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
        


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
    from modules.submacros.convertAhkPattern import ahkPatternToPython
    import os

    if sys.platform == "darwin" and sys.version_info[1] <= 7:
        multiprocessing.set_start_method("spawn")
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
    logger = logModule.log(log, False, None, blocking=True)

    #update settings
    profileSettings = settingsManager.loadSettings()
    profileSettingsReference = settingsManager.readSettingsFile("./data/default_settings/settings.txt")
    settingsManager.saveDict("../settings/profiles/a/settings.txt", {**profileSettingsReference, **profileSettings})

    #update general settings
    generalSettings = settingsManager.readSettingsFile("../settings/generalsettings.txt")
    generalSettingsReference = settingsManager.readSettingsFile("./data/default_settings/generalsettings.txt")
    settingsManager.saveDict("../settings/generalsettings.txt", {**generalSettingsReference, **generalSettings})

    #discord bot
    if generalSettings["discord_bot"]:
        discordBotProc = multiprocessing.Process(target=discordBot, args=(settingsManager.loadAllSettings()["discord_bot_token"], run, status))
        if settingsManager.loadAllSettings()["discord_bot"]:
            discordBotProc.start()

    #check if the user updated the paths (update 6)
    #TODO: remove this on the actual release
    with open("../settings/paths/cannon_to_field/blue flower.py", "r") as f:
        blueFlowerPath = f.read()
    f.close()

    compareBlueFlowerPath = '\nself.keyboard.press(",")\nself.keyboard.press(",")\nself.keyboard.slowPress("e")\nsleep(0.08)\nself.keyboard.keyDown("w")\nself.keyboard.slowPress("space")\nself.keyboard.slowPress("space")\nsleep(3)\nself.keyboard.keyUp("w")\nself.keyboard.slowPress("space")\nsleep(0.8)'
    if blueFlowerPath != compareBlueFlowerPath:
        messageBox.msgBox("Warning", "It looks like you did not update your paths for update 6. The macro will not work properly. Refer to update 6's instructions in #updates")
    
    #convert ahk pattern
    ahkPatterns = [x for x in os.listdir("../settings/patterns") if ".ahk" in x]
    for pattern in ahkPatterns:
        with open(f"../settings/patterns/{pattern}", "r") as f:
            ahk = f.read()
        f.close()
        python = ahkPatternToPython(ahk)
        print(f"Converted: {pattern}")
        patternName = pattern.rsplit(".", 1)[0].lower()
        with open(f"../settings/patterns/{patternName}.py", "w") as f:
            f.write(python)
        f.close()

    def stopApp(page= None, sockets = None):
        global stopThreads
        stopThreads = True
        print("stop")
        #print(sockets)
        macroProc.kill()
        # if discordBotProc.is_alive(): discordBotProc.kill()
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
            macroProc = multiprocessing.Process(target=macro, args=(status, log, haste, updateGUI), daemon=True)
            macroProc.start()
            #disconnect detection
            disconnectThread = Thread(target=disconnectCheck, args=(run, status, screenInfo["display_type"]))
            disconnectThread.daemon = True
            disconnectThread.start()
            #haste compensation
            if setdat["haste_compensation"]:
                hasteCompThread = Thread(target=hasteCompensationThread, args=(setdat["movespeed"], screenInfo["display_type"] == "retina", haste,))
                hasteCompThread.daemon = True
                hasteCompThread.start()

            #reset hourly report stats
            hourlyReportMainData = settingsManager.readSettingsFile("data/user/hourly_report_main.txt")
            for k in hourlyReportMainData:
                hourlyReportMainData[k] = 0   
            settingsManager.saveDict(f"data/user/hourly_report_main.txt", hourlyReportMainData)

            hourlyReportBgData = settingsManager.readSettingsFile("data/user/hourly_report_bg.txt")
            for k in hourlyReportBgData:
                if isinstance(hourlyReportBgData[k], list):
                    hourlyReportBgData[k] = []
                else:
                    hourlyReportBgData[k] = 0   
            settingsManager.saveDict(f"data/user/hourly_report_bg.txt", hourlyReportBgData)

            if setdat["enable_webhook"]:
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
            macroProc = multiprocessing.Process(target=macro, args=(status, log, haste, updateGUI), daemon=True)
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
    
            
            
            
