import eel
import webbrowser
eel.init('webapp')

@eel.expose
def openLink(link):
    webbrowser.open(link)

eel.start('index.html',app_mode = True)
