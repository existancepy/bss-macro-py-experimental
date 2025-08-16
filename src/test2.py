import time
import json

setdat = {} #settings
nectarNames=["comforting", "refreshing", "satisfying", "motivating", "invigorating"]
nectarFields = {
  "comforting": ["dandelion", "bamboo", "pine tree"],
  "refreshing": ["coconut", "strawberry", "blue flower"],
  "satisfying": ["pineapple", "sunflower", "pumpkin"],
  "motivating": ["stump", "spider", "mushroom", "rose"],
  "invigorating": ["pepper", "mountain top", "clover", "cactus"]
}
allPlanters = ["paper", "ticket", "festive", "sticker", "plastic", "candy", "red_clay", "blue_clay", "tacky", "pesticide", "heat-treated", "hydroponic", "petal", "planter_of_plenty"]
planters = [] #stores the planter name
planterNectars = [] #stores the nectar of planters placed down
planterFields = [] #stores the fields of the planters placed down
planterHarvestTimes = [] #stores the harvest times of the planters
lastNectarFields = { #stores the last field that was used for each nectar
  "comforting": "",
  "refreshing": "",
  "satisfying": "",
  "motivating": "",
  "invigorating": ""
}
planterEstPercent = []
with open("auto_planter_ranking.json", "r") as f:
    planterRankings = json.load(f) 

currentFieldNectar = None
CurrentField = "?" #most likely the current gather field
for i, nectar in enumerate(nectarNames):
    for j, field in enumerate(nectarFields[nectar]): 
        if CurrentField == field:
            currentFieldNectar = nectar
            break

def getNectarPerc(nectar):
    '''
    Detect nectar on screen and return its percentage (use hourly report's)?
    '''
    return 0

def getlastfield(nectar):
    '''
    Return the previous field used and the next field to plant in for the specified nectar
    '''
    arr = ["", ""]
    arr[0] = lastNectarFields[nectar]
    availableFields = []
    for field in nectarFields[nectar]:
        if setdat[f"auto_field_{field}"] and not field in planterFields:
            availableFields.append(field)
    if not availableFields:
        arr[1] = None
    #get the next field to plant in
    for i, field in enumerate(availableFields):
        if field == lastNectarFields[nectar]:
            nextFieldIndex = i+1
            if nextFieldIndex >= len(availableFields):
                nextFieldIndex = 0
            arr[1] = availableFields[nextFieldIndex]
            break
    else: #couldnt find the previous field in the available fields
        arr[0] = availableFields[0]
        arr[1] = availableFields[1] if len(availableFields) > 1 else availableFields[0]
    return availableFields

def getNextPlanter(field):
    nextPlanterData = None
    for planterObj in planterRankings[field]:
        name = planterObj["name"]
        settingName = name.replace(" ", "_")
        if not name in planters and setdat[f"auto_planter_{settingName}"]:
            nextPlanterData = planterObj
    return nextPlanterData

def savePlanter(field, planter, nectar):
    estimatedNectarPercent = getNectarPerc(nectar)
    #calculate the amount of nectar from planters currently placed down
    for j in range(3):
        if planterNectars[j] == nectar:
            estimatedNectarPercent += planterEstPercent[j]

    timeToCap = max(0.25, ((max(0, (100 - estimatedNectarPercent) / planter["nectar bonus"]) * 0.24) / planter["grow bonus"]))
    for i in range(5):
        if setdat[f"auto_priority_{i}_nectar"] == nectar:
            minPercent = max(setdat[f"auto_priority_{i}_min"], estimatedNectarPercent)
            break
    
    if planter["nectar bonus"] * planter["grow bonus"] < 1.2:
        autoInterval = min(timeToCap, 0.5)
    #haven't reached min percent and current nectar is a low amount
    elif minPercent > estimatedNectarPercent and estimatedNectarPercent <=90:
        if estimatedNectarPercent > 0:
            bonusTime = (100/estimatedNectarPercent)*planter["nectar bonus"]*planter["grow bonus"]
            autoInterval = (((minPercent - estimatedNectarPercent + bonusTime) / planter["nectar bonus"]) * 0.24) / planter["grow bonus"]
        else: #no nectar
            autoInterval = planter["grow time"]
    else: #already met minimum percent
        autoInterval = timeToCap
    
    if setdat["auto_planters_collect_auto"]:
        planterHarvestInterval = min(planter["grow time"], (autoInterval+autoInterval/(planter["nectar bonus"]*planter["grow bonus"])), timeToCap+timeToCap/(planter["nectar bonus"]*planter["grow bonus"]))
        planterHarvestTime = time.time() + planterHarvestInterval
    elif setdat["auto_planters_collect_full"]:
        planterHarvestInterval = planter["grow time"]
        planterHarvestTime = time.time() + planterHarvestInterval
    else:
        planterHarvestInterval = min(planter["grow time"], setdat["auto_planters_collect_every"])
        lowestHarvestTime = time.time() + planterHarvestInterval
        #sync harvest times with planters that are currently growing
        for i in range(3):
            harvestTime = planterHarvestTimes[i]
            if harvestTime > time.time() and lowestHarvestTime > harvestTime:
                lowestHarvestTime = harvestTime

        planterHarvestTime = lowestHarvestTime
        planterHarvestInterval = lowestHarvestTime - time.time()
    
    planterEstPerc = round((planterHarvestInterval * planter["nectar bonus"]/864), 1)

for i in range(5):
    nectar = setdat[f"auto_priority_{i}_nectar"]
    if nectar == "none":
        continue
    estimatedNectarPercent = 0
    #calculate the amount of nectar from planters currently placed down
    for j in range(3):
        if planterNectars[j] == nectar:
            estimatedNectarPercent += planterEstPercent[j]
    #get the current nectar%
    currentNectarPerc = getNectarPerc(nectar)
    #collect planters that are collecting the same type of nectar as current field but not in current field
    #probably exclude this
    if nectar == currentFieldNectar and not setdat["auto_planters_collect_full"]:
        for j in range(3):
            if CurrentField != planterFields[j] and currentFieldNectar == planterNectars[j]:
                temp = planterFields[j]
                planterHarvestTimes[j] = 0

    #collect all planters that will overfill nectar
    if (not setdat["auto_planters_collect_full"] and (
        (currentNectarPerc > 99) or
        (currentNectarPerc > 90 and currentNectarPerc + estimatedNectarPercent > 110) or
        (currentNectarPerc + estimatedNectarPercent > 120)
        )):
        for j in range(3):
            if (nectar == planterNectars[j]):
                planterHarvestTimes[j] = 0
    
#actually collect planters here
for i in range(3):
    if time.time() > planterHarvestTimes[i]:
        #runtask collect planter
        pass

#place planters
#1. meet nectar thresholds based on priority order

#determine max number of planters
#sanity check in case the user sets max planters to a value higher than the actual number of planters enabled
maxplanters = 0
for x in allPlanters:
    x = x.replace(" ","_")
    if setdat[f"auto_planter_{x}"]:
        maxplanters += 1

maxplanters = min(maxplanters, setdat["auto_max_planters"])

for i in range(5):
    nectar = setdat[f"auto_priority_{i}_nectar"]
    if nectar == "none":
        continue
    #get the maximum number of planters that can be placed for this specific nectar
    maxNectarPlanters = 0
    for field in nectarFields[nectar]:
        field = field.replace(" ","_")
        if setdat[f"auto_field_{field}"]:
            maxNectarPlanters += 1
    #get the number of planters currently placed for this specific nectar
    nectarPlantersPlaced = 0
    for j in range(3):
        if planterNectars[j] == nectar:
            nectarPlantersPlaced += 1
    #get the available slots to place in
    planterSlots = []
    for j in range(3):
        if not planters[j]:
            planterSlots.append(j)
    plantersPlaced = 3-planterSlots
    #keep placing planters until there are no slots left
    for _, e in enumerate(planterSlots):
        lastnextfield = getlastfield(nectar)
        lastField, nextField = lastnextfield
        
        nextPlanter = getNextPlanter(nextField)

        if nextField is None or nextPlanter is None or plantersPlaced >= maxplanters:
            break

        nectarPerc = getNectarPerc(nectar)
        minPerc = setdat[f"auto_priority_{i}_min"]
        estimatedNectarPercent = 0
        for j in range(3):
            if planterNectars[j] == nectar:
                estimatedNectarPercent += planterEstPercent[j]
        if estimatedNectarPercent + nectarPerc > minPerc:
            break
        #place planter
        #runTask(placePlanter)
        savePlanter(field, nextPlanter, nectar)
        plantersPlaced += 1
    
#handle leftover planters
#prioritise lowest nectar percentage
    

