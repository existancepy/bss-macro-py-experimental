import eel
import webbrowser
import modules.misc.settingsManager as settingsManager

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

eel.expose(settingsManager.loadFields)
eel.expose(settingsManager.saveField) 
eel.expose(settingsManager.loadSettings)
eel.expose(settingsManager.saveProfileSetting)


def toggleStartStop():
    eel.toggleStartStop()

def launch():
    eel.start('index.html',app_mode = True, block = False)
