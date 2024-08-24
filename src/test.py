import modules.submacros.fieldDriftCompensation as fdc
import modules.misc.appManager as appManager
import time

cl = fdc.fieldDriftCompensation(False)
appManager.openApp("roblox")
time.sleep(2)
cl.run()
