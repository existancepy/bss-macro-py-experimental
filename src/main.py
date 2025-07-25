
from modules.misc import messageBox
#check if step 3 installing dependencies was ran
try:
    import requests
except ModuleNotFoundError:
    messageBox.msgBox(title="Dependencies not installed", text="It seems like you have not finished step 3 of the installation process. Refer to https://existance-macro.gitbook.io/existance-macro-docs/macro-installation/markdown/2.-installing-dependencies")
from pynput import keyboard
import multiprocessing
import ctypes
from threading import Thread
import eel
import time
import sys
import ast
import subprocess
import atexit
from modules.misc.imageManipulation import adjustImage
from modules.screen.imageSearch import locateImageOnScreen
import pyautogui as pag
from modules.misc.appManager import getWindowSize
import traceback
import modules.misc.settingsManager as settingsManager
import modules.macro as macroModule
import modules.controls.mouse as mouse

try:
	from modules.misc.ColorProfile import DisplayColorProfile
except ModuleNotFoundError:
	messageBox.msgBox(title="Dependencies not installed", text="The new update requires new dependencies. Refer to https://existance-macro.gitbook.io/existance-macro-docs/macro-installation/markdown/2.-installing-dependencies.")
	quit()
from modules.submacros.hourlyReport import HourlyReport
mw, mh = pag.size()

#controller for the macro
def macro(status, logQueue, updateGUI):
    macro = macroModule.macro(status, logQueue, updateGUI)
    #invert the regularMobsInFields dict
    #instead of storing mobs in field, store the fields associated with each mob
    regularMobData = {}
    for k,v in macroModule.regularMobTypesInFields.items():
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

    taskCompleted = True
    questCache = {}
    
    macro.start()
    #macro.useItemInInventory("blueclayplanter")
    #function to run a task
    #makes it easy to do any checks after a task is complete (like stinger hunt, rejoin every, etc)
    def runTask(func = None, args = (), resetAfter = True, convertAfter = True):
        nonlocal taskCompleted
        #execute the task
        if func:
            returnVal = func(*args) 
            taskCompleted = True
        else:
            returnVal = None
        #task done
        if resetAfter: 
            macro.reset(convert=convertAfter)

        #do priority tasks
        if macro.night and macro.setdat["stinger_hunt"]:
            macro.stingerHunt()
        if macro.setdat["mondo_buff"] and macro.hasMondoRespawned():
            macro.collectMondoBuff()
        if macro.setdat["rejoin_every"]:
            if macro.hasRespawned("rejoin_every", macro.setdat["rejoin_every"]*60*60):
                macro.rejoin("Rejoining (Scheduled)")
                macro.saveTiming("rejoin_every")
        
        #auto field boost
        if macro.setdat["Auto_Field_Boost"] and not macro.AFBLIMIT:
            if macro.hasAFBRespawned("AFB_dice_cd", macro.setdat["AFB_rebuff"]*60) or macro.hasAFBRespawned("AFB_glitter_cd", macro.setdat["AFB_rebuff"]*60-30):
                macro.AFB(gatherInterrupt=False)

        status.value = ""
        return returnVal
    
    def handleQuest(questGiver):
        nonlocal questCache, taskCompleted
        
        gatherFieldsList = []
        gumdropGatherFieldsList = []
        requireRedField = False
        requireBlueField = False
        requireField = False
        requireBlueGumdropField = False
        requireRedGumdropField = False
        feedBees = []
        setdatEnable = []

        #if the macro has completed a task in the last cycle
        # if taskCompleted or not questGiver in questCache:
        #     questObjective = macro.findQuest(questGiver)
        #     questCache[questGiver] = questObjective
        # else:
        #     questObjective = questCache[questGiver]
        questObjective = macro.findQuest(questGiver)

        if questObjective is None:  # Quest does not exist
            questObjective = macro.getNewQuest(questGiver, False)
        elif not len(questObjective):  # Quest completed
            questObjective = macro.getNewQuest(questGiver, True)
            macro.hourlyReport.addHourlyStat("quests_completed", 1)

        if questObjective is None: #still not able to find quest
            return setdatEnable, gatherFieldsList, gumdropGatherFieldsList, requireRedField, requireBlueField, feedBees, requireRedGumdropField, requireBlueGumdropField, requireField

        for obj in questObjective:
            objData = obj.split("_")
            if objData[0] == "gather":
                gatherFieldsList.append(objData[1])
            elif objData[0] == "gathergoo":
                if macro.setdat["quest_use_gumdrops"]:
                    gumdropGatherFieldsList.append(objData[1])
                else:
                    gatherFieldsList.append(objData[1])
            elif objData[0] == "kill":
                if "ant" in objData[1] and objData[1] != "mantis":
                    setdatEnable.append("ant_challenge")
                    setdatEnable.append("ant_pass_dispenser")
                else:
                    setdatEnable.append(objData[2])
            elif objData[0] == "token":
                if questGiver == "riley bee":
                    requireRedField = True
                elif questGiver == "bucko bee":
                    requireBlueField = True
                else:
                    requireField = True

            elif objData[0] == "token" and objData[1] == "honeytoken":
                setdatEnable.append("honeytoken")
            elif objData[0] == "fieldtoken" and objData[1] == "blueberry":
                requireBlueField = True
            elif objData[0] == "fieldtoken" and objData[1] == "strawberry":
                requireRedField = True
            elif objData[0] == "feed":
                if objData[1] == "*":
                    amount = 25
                else:
                    amount = int(objData[1])
                feedBees.append((objData[2], amount))
            elif objData[0] == "pollen" and objData[1] == "blue":
                requireBlueField = True
            elif objData[0] == "pollen" and objData[1] == "red":
                requireRedField = True
            elif objData[0] == "pollengoo" and objData[1] == "blue":
                if macro.setdat["quest_use_gumdrops"]:
                    requireBlueGumdropField = True
                else:
                    requireBlueField = True
            elif objData[0] == "pollengoo" and objData[1] == "red":
                if macro.setdat["quest_use_gumdrops"]:
                    requireRedGumdropField = True
                else:
                    requireBlueField = True
            elif objData[0] == "collect":
                setdatEnable.append(objData[1].replace("-","_"))
        
        return setdatEnable, gatherFieldsList, gumdropGatherFieldsList, requireRedField, requireBlueField, feedBees, requireRedGumdropField, requireBlueGumdropField, requireField

    #macro.rejoin()
    while True:
        macro.setdat = settingsManager.loadAllSettings()
        #run empty task
        #this is in case no other settings are selected 
        runTask(resetAfter=False)

        #handle quests
        questGatherFields = []
        questGumdropGatherFields = []
        redFieldNeeded = False
        blueFieldNeeded = False
        fieldNeeded = False
        itemsToFeedBees = []
        redGumdropFieldNeeded = False
        blueGumdropFieldNeeded = False

        for questName, enabledKey in [
            ("polar bear", "polar_bear_quest"),
            ("honey bee", "honey_bee_quest"),
            ("bucko bee", "bucko_bee_quest"),
            ("riley bee", "riley_bee_quest")
        ]:
            if macro.setdat.get(enabledKey):
                setdatEnable, gatherFields, gumdropFields, needsRed, needsBlue, feedBees, needsRedGumdrop, needsBlueGumdrop, needsField = handleQuest(questName)
                for k in setdatEnable:
                    macro.setdat[k] = True
                questGatherFields.extend(gatherFields)
                questGumdropGatherFields.extend(gumdropFields)
                redFieldNeeded = redFieldNeeded or needsRed
                blueFieldNeeded = blueFieldNeeded or needsBlue
                itemsToFeedBees.extend(feedBees)
                redGumdropFieldNeeded = redGumdropFieldNeeded or needsRedGumdrop
                blueGumdropFieldNeeded = blueGumdropFieldNeeded or needsBlueGumdrop
                fieldNeeded = fieldNeeded or needsField
        
                    
        taskCompleted = False 

        #feed bees for quest
        for item, quantity in itemsToFeedBees:
            macro.feedBee(item, quantity)
            taskCompleted = True

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

        #planters
        def goToNextCycle(cycle, slot):
            #go to the next cycle
            for _ in range(8):
                cycle += 1
                if cycle > 5:
                    cycle = 1
                if macro.setdat[f"cycle{cycle}_{slot+1}_planter"] != "none" and macro.setdat[f"cycle{cycle}_{slot+1}_field"] != "none":
                    return cycle
            else: 
                return False
        
        planterDataRaw = None
        if macro.setdat["planters_mode"] == 1:
            with open("./data/user/manualplanters.txt", "r") as f:
                planterDataRaw = f.read()
            f.close()
            #no data, place planters
            if not planterDataRaw.strip():
                planterData = { #planter data to be stored in a file
                    "cycles": [1,1,1],
                    "planters": ["","",""],
                    "fields": ["","",""],
                    "gatherFields": ["","",""],
                    "harvestTimes": [0,0,0]
                }
                for i in range(3):
                    if macro.setdat[f"cycle1_{i+1}_planter"] == "none" or macro.setdat[f"cycle1_{i+1}_field"] == "none":
                        continue
                    planter = runTask(macro.placePlanterInCycle, args = (i, 1),resetAfter=False)
                    if planter:
                        planterData["planters"][i] = planter[0]
                        planterData["fields"][i] = planter[1]
                        planterData["harvestTimes"][i] = planter[2]
                        planterData["gatherFields"][i] = planter[1] if planter[3] else ""
                        with open("./data/user/manualplanters.txt", "w") as f:
                            f.write(str(planterData))
                        f.close()

            #planter data does exist, check if its time to collect them
            else: 
                planterData = ast.literal_eval(planterDataRaw)
                #check all 3 slots to see if planters are ready to harvest
                for i in range(3):
                    cycle = planterData["cycles"][i]
                    if planterData["planters"][i] and time.time() > planterData["harvestTimes"][i]:
                        #Collect planter
                        if runTask(macro.collectPlanter, args=(planterData["planters"][i], planterData["fields"][i])):
                            planterData["harvestTimes"][i] = ""
                            planterData["planters"][i] = ""
                            planterData["fields"][i] = ""
                            with open("./data/user/manualplanters.txt", "w") as f:
                                f.write(str(planterData))
                            f.close()

                #check for planters to place
                for i in range(3):
                    cycle = planterData["cycles"][i]
                    #check if planter slot is occupied
                    if planterData["planters"][i]:
                        continue
                    #if that planter is currently placed down by a different slot, do not harvest and place
                    #this avoids overlapping the same planter
                    nextCycle = goToNextCycle(cycle, i)
                    if not nextCycle: #make sure the column (slot) isnt just empty
                        continue

                    planterToPlace = macro.setdat[f"cycle{nextCycle}_{i+1}_planter"]
                    otherSlotPlanters = planterData["planters"][:i] + planterData["planters"][i+1:]
                    if planterToPlace in otherSlotPlanters:
                        continue

                    #also check for fields
                    fieldToPlace = macro.setdat[f"cycle{nextCycle}_{i+1}_field"]
                    otherSlotFields = planterData["fields"][:i] + planterData["fields"][i+1:]
                    if fieldToPlace in otherSlotFields:
                        continue
                    
                    #place planter
                    planter = runTask(macro.placePlanterInCycle, args = (i, nextCycle),resetAfter=False)
                    if planter:
                        planterData["cycles"][i] = nextCycle
                        planterData["planters"][i] = planter[0]
                        planterData["fields"][i] = planter[1]
                        planterData["harvestTimes"][i] = planter[2]
                        planterData["gatherFields"][i] = planter[1] if planter[3] else ""
                        with open("./data/user/manualplanters.txt", "w") as f:
                            f.write(str(planterData))
                        f.close()
                    
                 
        #mob run
        for mob, fields in regularMobData.items():
            if not macro.setdat[mob]: continue
            for f in fields:
                if macro.hasMobRespawned(mob, f):
                    runTask(macro.killMob, args=(mob, f,), convertAfter=False)
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
        #field boosters
        boostedGatherFields = []
        for k, _ in macroModule.fieldBoosterData.items():
            #check if the cooldown is up
            if macro.setdat[k] and macro.hasRespawned(k, macro.collectCooldowns[k]) and macro.hasRespawned("last_booster", macro.setdat["boost_seperate"]*60):
                boostedField = runTask(macro.collect, args=(k,))
                if macro.setdat["gather_boosted"] and boostedField:
                    boostedGatherFields.append(boostedField)

        allGatheredFields = []
        allGatheredFields.extend(boostedGatherFields)
        #gather in boosted fields
        #gather for the entire 15min duration
        for field in boostedGatherFields:
            st = time.time()
            while time.time() - st < 15*60:
                runTask(macro.gather, args=(field,), resetAfter=False)

        #add gather tab fields
        gatherFields = []
        for i in range(3):
            if macro.setdat["fields_enabled"][i]:
                gatherFields.append(macro.setdat["fields"][i])
        
        #add planter gather fields
        if planterDataRaw:
            planterGatherFields = [x for x in ast.literal_eval(planterDataRaw)["gatherFields"] if x]
        else:
            planterGatherFields = []
        gatherFields.extend([x for x in planterGatherFields if x not in gatherFields])

        #remove fields that are already in boosted fields
        gatherFields = [x for x in gatherFields if not x in boostedGatherFields]

        allGatheredFields.extend(gatherFields)
        
        for field in gatherFields:
            runTask(macro.gather, args=(field,), resetAfter=False)

        #do quests

        blueFields = ["blue flower", "bamboo", "pine tree", "stump"]
        redFields = ["mushroom", "strawberry", "rose", "pepper"]

        #setup the override
        questGatherOverrides = {}
        if macro.setdat["quest_gather_mins"]:
            questGatherOverrides["mins"] = macro.setdat["quest_gather_mins"]
        if macro.setdat["quest_gather_return"] != "no override":
            questGatherOverrides["return"] = macro.setdat["quest_gather_return"]
            

        #do goo-field gathers first
        if blueGumdropFieldNeeded:
            for f in blueFields:
                if f in questGumdropGatherFields:
                    break
            else:
                questGumdropGatherFields.append("pine tree")
        
        if redGumdropFieldNeeded:
            for f in redFields:
                if f in questGumdropGatherFields:
                    break
            else:
                questGumdropGatherFields.append("rose")

        for field in questGumdropGatherFields:
            runTask(macro.gather, args=(field, questGatherOverrides, True), resetAfter=False)
        allGatheredFields.extend(questGumdropGatherFields)


        #do regular gathers
        questGatherFields = [x for x in questGatherFields if not (x in allGatheredFields)]
        for field in questGatherFields:
            runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
        allGatheredFields.extend(questGatherFields)

        #do required blue/red fields
        if blueFieldNeeded:
            for f in blueFields:
                if f in allGatheredFields:
                    break
            else:
                field = "pine tree"
                allGatheredFields.append(field)
                runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
        
        if redFieldNeeded:
            for f in redFields:
                if f in allGatheredFields:
                    break
            else:
                field = "rose"
                allGatheredFields.append(field)
                runTask(macro.gather, args=(field, questGatherOverrides), resetAfter=False)
        
        if fieldNeeded and not allGatheredFields:
            runTask(macro.gather, args=("pine tree",), resetAfter=False)
        
        mouse.click()
        
        


def watch_for_hotkeys(run):
    def on_press(key):
        nonlocal run
        if key == keyboard.Key.f1:
            
            if run.value == 2: #already running
                print("Already running")
                return 
            run.value = 1
        elif key == keyboard.Key.f3:
            if run.value == 3: #already stopped
                print("Already stopped")
                return
            run.value = 0

    keyboard.Listener(on_press=on_press).start()

if __name__ == "__main__":
    print("Loading gui...")
    global stopThreads, macroProc
    import gui
    import modules.screen.screenData as screenData
    from modules.controls.keyboard import keyboard as keyboardModule
    import modules.logging.log as logModule
    import modules.misc.appManager as appManager
    import modules.misc.settingsManager as settingsManager
    from modules.discord_bot.discordBot import discordBot
    from modules.submacros.convertAhkPattern import ahkPatternToPython
    from modules.submacros.stream import cloudflaredStream
    import os

    if sys.platform == "darwin" and sys.version_info[1] <= 7:
        print("start method set to spawn")
        multiprocessing.set_start_method("spawn")
    macroProc = None
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
    logQueue = manager.Queue()
    watch_for_hotkeys(run)
    logger = logModule.log(logQueue, False, None, blocking=True)

    disconnectCooldownUntil = 0 #only for running disconnect check on low performance

    #update settings
    profileSettings = settingsManager.loadSettings()
    profileSettingsReference = settingsManager.readSettingsFile("./data/default_settings/settings.txt")
    settingsManager.saveDict("../settings/profiles/a/settings.txt", {**profileSettingsReference, **profileSettings})

    #update general settings
    generalSettings = settingsManager.readSettingsFile("../settings/generalsettings.txt")
    generalSettingsReference = settingsManager.readSettingsFile("./data/default_settings/generalsettings.txt")
    settingsManager.saveDict("../settings/generalsettings.txt", {**generalSettingsReference, **generalSettings})

    #convert ahk pattern
    ahkPatterns = [x for x in os.listdir("../settings/patterns") if ".ahk" in x]
    for pattern in ahkPatterns:
        with open(f"../settings/patterns/{pattern}", "r") as f:
            ahk = f.read()
        f.close()
        try:
            python = ahkPatternToPython(ahk)
            print(f"Converted: {pattern}")
            patternName = pattern.rsplit(".", 1)[0].lower()
            with open(f"../settings/patterns/{patternName}.py", "w") as f:
                f.write(python)
            f.close()
        except:
            messageBox.msgBox(title="Failed to convert pattern", text=f"There was an error converting {pattern}. The pattern will not be used.")
    
    #setup stream class
    stream = cloudflaredStream()

    def onExit():
        stopApp()
        try:
            if discordBotProc and discordBotProc.is_alive():
                discordBotProc.terminate()
                discordBotProc.join()
        except NameError:
            pass
        
    def stopApp(page= None, sockets = None):
        global stopThreads
        global macroProc
        stopThreads = True
        print("stop")
        #print(sockets)
        if macroProc and macroProc.is_alive():
            macroProc.kill()
            macroProc.join()
            macroProc = None
        stream.stop()
        #if discordBotProc.is_alive(): discordBotProc.kill()
        keyboardModule.releaseMovement()
        mouse.mouseUp()
    
    atexit.register(onExit)
        
    #setup and launch gui
    gui.run = run
    gui.launch()
    #use run.value to control the macro loop

    #check color profile
    if sys.platform == "darwin":
        try:
            colorProfileManager = DisplayColorProfile()
            currentProfileColor = colorProfileManager.getCurrentColorProfile()
            if not "sRGB" in currentProfileColor:
                try:
                    if messageBox.msgBoxOkCancel(title="Incorrect Color Profile", text=f"You current display's color profile is {currentProfileColor} but sRGB is required for the macro.\nPress 'Ok' to change color profiles"):
                        colorProfileManager.resetDisplayProfile()
                        colorProfileManager.setCustomProfile("/System/Library/ColorSync/Profiles/sRGB Profile.icc")
                        messageBox.msgBox(title="Color Profile Success", text="Successfully changed the current color profile to sRGB")

                except Exception as e:
                    messageBox.msgBox(title="Failed to change color profile", text=e)
        except Exception as e:
            pass
    
        #check screen recording permissions
        try:
            cg = ctypes.cdll.LoadLibrary("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")
            cg.CGRequestScreenCaptureAccess.restype = ctypes.c_bool
            if not cg.CGRequestScreenCaptureAccess():
                messageBox.msgBox(title="Screen Recording Permission", text='Terminal does not have the screen recording permission. The macro will not work properly.\n\nTo fix it, go to System Settings -> Privacy and Security -> Screen Recording -> add and enable Terminal. After that, restart the macro')
        except AttributeError:
            pass
        #check full keyboard access
        try:
            result = subprocess.run(
                ["defaults", "read", "com.apple.universalaccess", "KeyboardAccessEnabled"],
                capture_output=True,
                text=True
            )
            value = result.stdout.strip()
            if value == "1":
                messageBox.msgBox(text = f"Full Keyboard Access is enabled. The macro will not work properly\
                    \nTo disable it, go to System Settings -> Accessibility -> Keyboard -> uncheck 'Full Keyboard Access'")
        except Exception as e:
            print("Error reading Full Keyboard Access:", e)

    discordBotProc = None
    prevDiscordBotToken = None

    while True:
        eel.sleep(0.5)
        setdat = settingsManager.loadAllSettings()

        #discord bot. Look for changes in the bot token
        currentDiscordBotToken = setdat["discord_bot_token"]
        if setdat["discord_bot"] and currentDiscordBotToken and currentDiscordBotToken != prevDiscordBotToken:
            if discordBotProc is not None and discordBotProc.is_alive():
                print("Detected change in discord bot token, killing previous bot process")
                discordBotProc.terminate()
                discordBotProc.join()
            discordBotProc = multiprocessing.Process(target=discordBot, args=(currentDiscordBotToken, run, status), daemon=True)
            prevDiscordBotToken = currentDiscordBotToken
            discordBotProc.start()

        if run.value == 1:
            print("start")
            #create and set webhook obj for the logger
            logger.enableWebhook = setdat["enable_webhook"]
            logger.webhookURL = setdat["webhook_link"]
            print("Setting stop threads")
            stopThreads = False
            print("variables initalised")

            #reset hourly report data
            hourlyReport = HourlyReport()
            hourlyReport.resetAllStats()
            #stream
            def waitForStreamURL():
                #wait for up to 15 seconds for the public link
                for _ in range(150):
                    time.sleep(0.1)
                    if stream.publicURL:
                        logger.webhook("Stream Started", f'Stream URL: {stream.publicURL}', "purple")
                        return
            
                logger.webhook("", f'Stream could not start. Check terminal for more info', "red")

            print("checking stream")
            streamLink = None
            if setdat["enable_stream"]:
                print("stream enabled")
                if stream.isCloudflaredInstalled():
                    logger.webhook("", "Starting Stream...", "light blue")
                    streamLink = stream.start(setdat["stream_resolution"])
                    Thread(target=waitForStreamURL, daemon=True).start()
                else:
                    messageBox.msgBox(text='Cloudflared is required for streaming but is not installed. Visit https://existance-macro.gitbook.io/existance-macro-docs/guides/optional-installations/stream-setup-installing-cloudflared for installation instructions', title='Cloudflared not installed')

            print("starting macro proc")
            #check if user enabled field drift compensation but sprinkler is not supreme saturator
            fieldSettings = settingsManager.loadFields()
            sprinkler = setdat["sprinkler_type"]
            for field in setdat["fields"]:
                if fieldSettings[field]["field_drift_compensation"] and setdat["sprinkler_type"] != "saturator":
                    messageBox.msgBox(title="Field Drift Compensation", text=f"You have Field Drift Compensation enabled for {field} field, \
                                    but you do not have Supreme Saturator as your sprinkler type in configs.\n\
				                    Field Drift Compensation requires you to own the Supreme Saturator.\n\
                                    Kindly disable field drift compensation if you do not have the Supreme Saturator")
                    break
            #check if blender is enabled but there are no items to craft
            validBlender = not setdat["blender_enable"] #valid blender set to false if blender is enabled, else its true since blender is disabled
            for i in range(1,4):
                if setdat[f"blender_item_{i}"] != "none" and (setdat[f"blender_repeat_{i}"] or setdat[f"blender_repeat_inf_{i}"]):
                    validBlender = True
            if not validBlender:
                messageBox.msgBox(title="Blender", text=f"You have blender enabled, \
                                    but there are no more items left to craft.\n\
				                    Check the 'repeat' setting on your blender items and reset blender data.")
            #macro proc
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, updateGUI), daemon=True)
            macroProc.start()

            logger.webhook("Macro Started", f'Existance Macro v2.0\nDisplay: {screenInfo["display_type"]}, {screenInfo["screen_width"]}x{screenInfo["screen_height"]}', "purple")
            run.value = 2
            gui.toggleStartStop()
        elif run.value == 0:
            if macroProc:
                logger.webhook("Macro Stopped", "exih macro", "red")
                run.value = 3
                gui.toggleStartStop()
                stopApp()
        elif run.value == 4: #disconnected
            macroProc.kill()
            logger.webhook("","Disconnected", "red", "screen")
            appManager.closeApp("Roblox")
            keyboardModule.releaseMovement()
            mouse.mouseUp()
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, updateGUI), daemon=True)
            macroProc.start()
            run.value = 2
        
        #Check for crash
        if macroProc and not macroProc.is_alive() and hasattr(macroProc, "exitcode") and macroProc.exitcode is not None and macroProc.exitcode < 0:
            logger.webhook("","Crashed", "red", "screen")
            macroProc.join()
            appManager.openApp("Roblox")
            keyboardModule.releaseMovement()
            mouse.mouseUp()
            macroProc = multiprocessing.Process(target=macro, args=(status, logQueue, updateGUI), daemon=True)
            macroProc.start()

        #detect a new log message
        if not logQueue.empty():
            logData = logQueue.get()
            if logData["type"] == "webhook": #webhook
                msg = f"{logData['title']}<br>{logData['desc']}"

            #add it to gui
            gui.log(logData["time"], msg, logData["color"])
        
        #detect if the gui needs to be updated
        if updateGUI.value:
            gui.updateGUI()
            updateGUI.value = 0
        
        if run.value == 2 and time.time() > disconnectCooldownUntil:
            img = adjustImage("./images/menu", "disconnect", screenInfo["display_type"])
            wmx, wmy, wmw, wmh = getWindowSize("roblox roblox")
            if locateImageOnScreen(img, wmx+wmw/3, wmy+wmh/2.8, wmw/2.3, wmh/5, 0.7):
                print("disconnected")
                run.value = 4
                disconnectCooldownUntil = time.time() + 300  # 5 min cooldown
    
            
            
        
