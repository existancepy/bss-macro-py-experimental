import time
print(time.time()-1751551061.93558)
print(time.time())
import ast

with open("./data/user/manualplanters.txt", "r") as f:
    planterDataRaw = f.read()
f.close()

planterData = ast.literal_eval(planterDataRaw)

def displayTime(seconds, units = ['w','d','h','m','s']):
    intervals = (
        ('w', 604800),  # 60 * 60 * 24 * 7
        ('d', 86400),    # 60 * 60 * 24
        ('h', 3600),    # 60 * 60
        ('m', 60),
        ('s', 1),
    )
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            if name in units:
                value = int(value)
                if value < 10:
                    value = "0"+str(value)
                result.append("{}{}".format(value, name))
    if not result:
        return "0s"
    return ' '.join(result)

planterNames = []
planterTimes = []
planterFields = []
for i in range(len(planterData["planters"])):
    if planterData["planters"][i]:
        planterNames.append(planterData["planters"][i])
        planterTimes.append(planterData["harvestTimes"][i] - time.time())
        planterFields.append(planterData["fields"][i])
print(planterTimes[0])
print(displayTime(-647.2801861763, ["m", "s"]))
