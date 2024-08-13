import eel
import webbrowser
import modules.misc.settingsManager as settingsManager
import os

eel.init('webapp')
run = None
@eel.expose
def openLink(link):
    webbrowser.open(link)
    
@eel.expose
def start():
    if run.value == 2: return #already running
    run.value = 1
    
@eel.expose
def stop():
    if run.value == 3: return #already stopped
    run.value = 0
@eel.expose
def getPatterns():
    return [x.replace(".py","") for x in os.listdir("../settings/patterns") if ".py" in x]

def log(time = "", msg = "", color = ""):
    eel.log(time, msg, color)

eel.expose(settingsManager.loadFields)
eel.expose(settingsManager.saveField) 
eel.expose(settingsManager.loadSettings)
eel.expose(settingsManager.loadAllSettings)
eel.expose(settingsManager.saveProfileSetting)
eel.expose(settingsManager.saveGeneralSetting)



def toggleStartStop():
    eel.toggleStartStop()

def launch():
    eel.start('index.html',app_mode = True, block = False)