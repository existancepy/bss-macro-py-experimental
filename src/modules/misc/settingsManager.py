import ast
#returns a dictionary containing the settings
profileName = "a"
def readSettingsFile(path):
    #get each line
    #read the file, format it to:
    #[[key, value], [key, value]]
    with open(path) as f:
        data = [[x.strip() for x in y.split("=")] for y in f.read().split("\n")]
    f.close()
    out = {}
    for k,v in data:
        try:
            out[k] = ast.literal_eval(v)
        except:
            out[k] = v
    return out

def saveDict(path, data):
    out = "\n".join([f"{k}={v}" for k,v in data.items()])
    with open(path, "w") as f:
        f.write(str(out))
    f.close()

#update one property of a setting
def saveSettingFile(setting,value, path):
    #get the dictionary
    data = readSettingsFile(path)
    #update the dictionary
    data[setting] = value
    #write it
    saveDict(path, data)

def loadFields():
    with open(f"../settings/profiles/{profileName}/fields.txt") as f:
        out = ast.literal_eval(f.read())
    f.close()
    return out

def saveField(field, settings):
    fieldsData = loadFields()
    fieldsData[field] = settings
    with open(f"../settings/profiles/{profileName}/fields.txt", "w") as f:
        f.write(str(fieldsData))
    f.close()

def saveProfileSetting(setting, value):
    saveSettingFile(setting, value, f"../settings/profiles/{profileName}/settings.txt")

def loadSettings():
    return readSettingsFile(f"../settings/profiles/{profileName}/settings.txt")

#return a dict containing all settings except field (general, profile, planters)
def loadAllSettings():
    return {**loadSettings()}
