from html2image import Html2Image
from pathlib import Path
from PIL import Image
import cv2
from modules.misc.settingsManager import readSettingsFile
import math
import time
import ast
import numpy as np
import platform
from modules.misc.messageBox import msgBox
from modules.screen.imageSearch import locateTransparentImageOnScreen
from modules.screen.screenshot import mssScreenshotNP, mssScreenshot
from modules.misc.imageManipulation import adjustImage
import time
import pyautogui as pag
from modules.screen.ocr import ocrRead
from modules.screen.screenData import getScreenData

ww, wh = pag.size()

def versionTuple(v):
    return tuple(map(int, (v.split("."))))
macVer = platform.mac_ver()[0]

try:
    hti = Html2Image(size=(1900, 780))
    if hasattr(hti.browser, 'use_new_headless'):
        hti.browser.use_new_headless = None

    
except FileNotFoundError:
    if versionTuple(macVer) >= versionTuple("10.15"):
        msgBox(title = "error", text = "Google Chrome could not be found. Ensure that:\
    \n1. Google Chrome is installed\nGoogle chrome is in the applications folder (open the google chrome dmg file. From the pop up, drag the icon into the folder)")
    else:
        hti = None

#buff size is 76x76
lower = np.array([0, 102, 0])
upper = np.array([110, 255, 31])
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
x = 0
y = 30

#key: name of buff
#value: [template for template matching is the buff's top, bottom or middle, if buff image should be transformed]
buffs = {
    "tabby_love": ["top", True],
    "polar_power": ["top", True],
    "wealth_clock": ["top", True],
    "blessing": ["middle", True],
    "bloat": ["top", True],
}
buffs = buffs.items()
buffQuantity = []

nectars = {
    "comforting": [[np.array([0, 150, 63]), np.array([20, 155, 70])], (-2,0)],
    "invigorating": [[np.array([0, 128, 95]), np.array([180, 132, 101])], (-2,4)],
    "motivating": [[np.array([160, 150, 63]), np.array([170, 155, 70])], (-2,-2)],
    "refreshing": [[np.array([50, 144, 70]), np.array([70, 151, 75])], (-2,2)],
    "satisfying": [[np.array([130, 163, 36]), np.array([140, 168, 40])], (-2,0)]
}
nectarKernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
nectars = nectars.items()


def getBuffs():
    buffQuantity = []
    displayType = getScreenData()["display_type"]
    for buff,v in buffs:
        templatePosition, transform = v
        multi = 2 if displayType == "retina" else 1

        #find the buff
        buffTemplate = adjustImage("./images/buffs", buff, displayType)
        res = locateTransparentImageOnScreen(buffTemplate, x, y, ww/1.8, 45, 0.7)
        if not res: 
            buffQuantity.append("0")
            continue

        #get a screenshot of the buff
        rx, ry = res[1]
        h,w = buffTemplate.shape[:-1]
        if templatePosition == "bottom": 
            ry-=78-h
        elif templatePosition == "middle":
            rx -= (78-w)/2+8
            ry -= 30
        fullBuffImgRAW = mssScreenshotNP(x+(rx/multi), y+ry/multi, 39, 39)

        #filter out everything but the text
        fullBuffImgBGR = cv2.cvtColor(fullBuffImgRAW, cv2.COLOR_RGBA2BGR)
        mask = cv2.cvtColor(fullBuffImgBGR, cv2.COLOR_BGR2HLS)
        if transform:
            mask = cv2.inRange(mask, lower, upper)
            mask = cv2.erode(mask, kernel)
        mask = Image.fromarray(mask)

        #mask.save(f"{time.time()}.png")
        #read the text
        ocrText = ''.join([x[1][0] for x in ocrRead(mask)]).replace(":", ".")
        buffCount = ''.join([x for x in ocrText if x.isdigit() or x == "."])
        print(buff)
        print(ocrText)

        buffQuantity.append(buffCount if buffCount else '1')
    return buffQuantity

def getNectars():
    nectarQuantity = []
    displayType = getScreenData()["display_type"]
    for buff, vals in nectars:
        col, offsetCoords = vals
        offsetX, offsetY = offsetCoords
        multi = 2 if displayType == "retina" else 1

        #find the buff
        buffTemplate = adjustImage("./images/buffs", buff, displayType)
        res = locateTransparentImageOnScreen(buffTemplate, x, y, ww/1.8, 45, 0.5) #get the best match first. At high nectar levels, it becomes hard to detect the nectar icon
        if not res: 
            nectarQuantity.append("0")
            continue
        #get a screenshot of the buff
        rx, ry = res[1]
        fullBuffImg = mssScreenshotNP(x+(rx/multi)+offsetX, y+ry/multi+offsetY, 40, 40)
        h,w, *_ = fullBuffImg.shape
        #get the buff level
        fullBuffImg = cv2.cvtColor(fullBuffImg, cv2.COLOR_RGBA2BGR)
        mask = cv2.cvtColor(fullBuffImg, cv2.COLOR_BGR2HLS)
        mask = cv2.inRange(mask, col[0], col[1])
        #cv2.imshow("mask", mask)
        #cv2.waitKey(0)
        mask = cv2.erode(mask, nectarKernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
        if not contours:
            #in this case, the nectar quantity might be so low it cant be detected or the player doesnt have the nectar at all
            #so, we get the confidence value of the match
            #if the value is high, its probably low nectar quantity
            #if its low, the player prob doesnt have the nectar
            max_val, _  = res
            nectarQuantity.append(2 if max_val > 0.8 else 0)
            continue
        # return the bounding with the largest area
        _, _, _, buffH = cv2.boundingRect(max(contours, key=cv2.contourArea))
        quantity = min(100, (buffH/h*100))
        nectarQuantity.append(quantity)
    return nectarQuantity

def millify(n):
    if not n: return "0"
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def filterOutliers(values, threshold=3):
    nonZeroValues = [x for x in values if x]
    # Calculate the mean and standard deviation
    mean = np.mean(nonZeroValues)
    std_dev = np.std(nonZeroValues)

    #standard deviation is 0, no outliers, prevent division by zero
    if std_dev == 0:
        return values 
    
    # Calculate Z-scores
    z_scores = [(x - mean) / std_dev for x in values]
    
    # Filter out values with Z-scores greater than the threshold
    filtered_values = [x for x, z in zip(values, z_scores) if abs(z) < threshold or not x]
    
    return filtered_values

intervals = (
    ('w', 604800),  # 60 * 60 * 24 * 7
    ('d', 86400),    # 60 * 60 * 24
    ('h', 3600),    # 60 * 60
    ('m', 60),
    ('s', 1),
)

def display_time(seconds, units = ['w','d','h','m','s']):
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
                result.append("{} {}".format(value, name))
    return ' '.join(result)

def generateHourlyReport24(newUI):
    global y
    if newUI: y=52
    pages = ["page1.html", "page2.html"]
    pageImages = []
    buffQuantity = getBuffs()
    nectarQuantity = getNectars()
    #mssScreenshot(save=True)
    for page in pages:
        #relative file paths do not work, so replace the paths in src with absolute paths
        hourlyReportDir = Path(__file__).parents[2] / "hourly_report"
        pageDir = hourlyReportDir / page
        pageName = page.split(".",1)[0]
        with open(pageDir, "r") as f:
            htmlString = f.read()
        f.close()

        #get the hourly report data
        hourlyReportData = {**readSettingsFile("data/user/hourly_report_main.txt"), **readSettingsFile("data/user/hourly_report_bg.txt")}

        #get planter data
        with open("./data/user/manualplanters.txt", "r") as f:
            planterData = f.read()
        f.close()

        #get history
        with open("data/user/hourly_report_history.txt", "r") as f:
            historyData = ast.literal_eval(f.read())
        f.close()
        
        if len(hourlyReportData["honey_per_min"]) < 3:
            hourlyReportData["honey_per_min"] = [0]*3 + hourlyReportData["honey_per_min"]
        #filter out the honey/min
        print(hourlyReportData["honey_per_min"])
        #hourlyReportData["honey_per_min"] = [x for x in hourlyReportData["honey_per_min"] if x]
        hourlyReportData["honey_per_min"] = filterOutliers(hourlyReportData["honey_per_min"])
        #calculate honey/min
        honeyPerMin = [0]
        prevHoney = hourlyReportData["honey_per_min"][0]
        for x in hourlyReportData["honey_per_min"][1:]:
            if x > prevHoney:
                honeyPerMin.append((x-prevHoney)/60)
            prevHoney = x
        
        #calculate some stats
        if len(set(hourlyReportData["honey_per_min"])) <= 1:
            onlyValidHourlyHoney = hourlyReportData["honey_per_min"].copy()
        else:
            onlyValidHourlyHoney = [x for x in hourlyReportData["honey_per_min"] if x] #removes all zeroes
        sessionHoney = onlyValidHourlyHoney[-1]- hourlyReportData["start_honey"]
        sessionTime = time.time()-hourlyReportData["start_time"]
        honeyThisHour = onlyValidHourlyHoney[-1] - onlyValidHourlyHoney[0]

        #replace the contents of the html
        replaceDict = {
            'src="a': f'src="{hourlyReportDir}/a'.replace("\\", "/"),
            '`as': '`{}/as'.format(str(hourlyReportDir).replace("\\", "/")),
            "-avgHoney": millify(sessionHoney/(sessionTime/3600)),
            "-honey": millify(honeyThisHour),
            "-bugs": hourlyReportData["bugs"],
            "-quests": hourlyReportData["quests_completed"],
            "-vicBees": hourlyReportData["vicious_bees"],
            "-currHoney": millify(onlyValidHourlyHoney[-1]),
            "-sessHoney": millify(sessionHoney),
            "-sessTime": display_time(sessionTime, ['d','h','m']),
            "var honeyPerMin = []": f'var honeyPerMin = {honeyPerMin}',
            "var backpackPerMin = []": f'var backpackPerMin = {hourlyReportData["backpack_per_min"]}',
            "const taskTimes = []": f'const taskTimes = [{hourlyReportData["gathering_time"]}, {hourlyReportData["converting_time"]}, {hourlyReportData["bug_run_time"]}, {hourlyReportData["misc_time"]}]',
            "const historyData = []": f'const historyData = {historyData}',
            "const honey = 0": f'const honey = {honeyThisHour}',
            "url(a": f'url({hourlyReportDir}/a'.replace("\\", "/"),
            "const buffNames = []": f'const buffNames = {[k for k,v in buffs]}',
            "const buffValues = []": f'const buffValues = {buffQuantity}',
            "const nectarValues = []": f'const nectarValues = {nectarQuantity}'
        }

        if planterData:
            planterData = ast.literal_eval(planterData)
            planterReplaceDict = {
                "const planterNames = []": f'const planterNames = {planterData["planters"]}', 
                "const planterTimes = []": f'const planterTimes = {[planterData["harvestTime"]-time.time()]*3}',
                "const planterFields = []": f'const planterFields = {planterData["fields"]}',
            }
            replaceDict = {**replaceDict, **planterReplaceDict}
        for k,v in replaceDict.items():
            htmlString = htmlString.replace(k,str(v))
        #save the html as an image
        hti.screenshot(html_str=htmlString, save_as=f"{pageName}.png")
        #open the image
        image = cv2.imread(f"{pageName}.png")
        #print(htmlString)

        #crop the image to remove any excess empty space at the bottom
        #this allows for seamless merging of images
        # Define the BGR color value for #0E0F13 (the background)
        targetColor = np.array([19, 15, 14])
        # Tolerance for matching the color
        tolerance = 5
        height, width, _ = image.shape
        # Function to check if a row contains the specified color
        def is_color_row(row):
            return np.all(np.abs(row - targetColor) < tolerance, axis=1).all()

        # Find the row where the empty space starts (from the bottom of the image going upwards)
        emptyAreaStart = height
        for row in range(height-1, -1, -1):
            if is_color_row(image[row, :]):
                emptyAreaStart = row
            else:
                break

        # Crop the image above the space
        image = image[:emptyAreaStart, :]

        pageImages.append(image)

    imgOut = cv2.vconcat(pageImages) 
    #Get the original dimensions
    height, width = imgOut.shape[:2]
    # Resize the image
    imgOut = cv2.resize(imgOut, (width*2, height*2))
    cv2.imwrite("hourlyReport.png", imgOut) 
    return hourlyReportData

def generateHourlyReport12(newUI):
    global y
    if newUI: y=52
    pages = ["page3.html", "page2.html"]
    pageImages = []
    buffQuantity = getBuffs()
    nectarQuantity = getNectars()
    #mssScreenshot(save=True)
    for page in pages:
        #relative file paths do not work, so replace the paths in src with absolute paths
        hourlyReportDir = Path(__file__).parents[2] / "hourly_report"
        pageDir = hourlyReportDir / page
        pageName = page.split(".",1)[0]
        with open(pageDir, "r") as f:
            htmlString = f.read()
        f.close()

        #get the hourly report data
        hourlyReportData = {**readSettingsFile("data/user/hourly_report_main.txt"), **readSettingsFile("data/user/hourly_report_bg.txt")}

        #get planter data
        with open("./data/user/manualplanters.txt", "r") as f:
            planterData = f.read()
        f.close()

        #get history
        with open("data/user/hourly_report_history.txt", "r") as f:
            historyData = ast.literal_eval(f.read())
        f.close()
        
        if len(hourlyReportData["honey_per_min"]) < 3:
            hourlyReportData["honey_per_min"] = [0]*3 + hourlyReportData["honey_per_min"]
        #filter out the honey/min
        print(hourlyReportData["honey_per_min"])
        #hourlyReportData["honey_per_min"] = [x for x in hourlyReportData["honey_per_min"] if x]
        hourlyReportData["honey_per_min"] = filterOutliers(hourlyReportData["honey_per_min"])
        #calculate honey/min
        honeyPerMin = [0]
        prevHoney = hourlyReportData["honey_per_min"][0]
        for x in hourlyReportData["honey_per_min"][1:]:
            if x > prevHoney:
                honeyPerMin.append((x-prevHoney)/60)
            prevHoney = x
        
        #calculate some stats
        if len(set(hourlyReportData["honey_per_min"])) <= 1:
            onlyValidHourlyHoney = hourlyReportData["honey_per_min"].copy()
        else:
            onlyValidHourlyHoney = [x for x in hourlyReportData["honey_per_min"] if x] #removes all zeroes
        sessionHoney = onlyValidHourlyHoney[-1]- hourlyReportData["start_honey"]
        sessionTime = time.time()-hourlyReportData["start_time"]
        honeyThisHour = onlyValidHourlyHoney[-1] - onlyValidHourlyHoney[0]

        #replace the contents of the html
        replaceDict = {
            'src="a': f'src="{hourlyReportDir}/a'.replace("\\", "/"),
            '`as': '`{}/as'.format(str(hourlyReportDir).replace("\\", "/")),
            "-avgHoney": millify(sessionHoney/(sessionTime/3600)),
            "-honey": millify(honeyThisHour),
            "-bugs": hourlyReportData["bugs"],
            "-quests": hourlyReportData["quests_completed"],
            "-vicBees": hourlyReportData["vicious_bees"],
            "-currHoney": millify(onlyValidHourlyHoney[-1]),
            "-sessHoney": millify(sessionHoney),
            "-sessTime": display_time(sessionTime, ['d','h','m']),
            "var honeyPerMin = []": f'var honeyPerMin = {honeyPerMin}',
            "var backpackPerMin = []": f'var backpackPerMin = {hourlyReportData["backpack_per_min"]}',
            "const taskTimes = []": f'const taskTimes = [{hourlyReportData["gathering_time"]}, {hourlyReportData["converting_time"]}, {hourlyReportData["bug_run_time"]}, {hourlyReportData["misc_time"]}]',
            "const historyData = []": f'const historyData = {historyData}',
            "const honey = 0": f'const honey = {honeyThisHour}',
            "url(a": f'url({hourlyReportDir}/a'.replace("\\", "/"),
            "const buffNames = []": f'const buffNames = {[k for k,v in buffs]}',
            "const buffValues = []": f'const buffValues = {buffQuantity}',
            "const nectarValues = []": f'const nectarValues = {nectarQuantity}'
        }

        if planterData:
            planterData = ast.literal_eval(planterData)
            planterReplaceDict = {
                "const planterNames = []": f'const planterNames = {planterData["planters"]}', 
                "const planterTimes = []": f'const planterTimes = {[planterData["harvestTime"]-time.time()]*3}',
                "const planterFields = []": f'const planterFields = {planterData["fields"]}',
            }
            replaceDict = {**replaceDict, **planterReplaceDict}
        for k,v in replaceDict.items():
            htmlString = htmlString.replace(k,str(v))
        #save the html as an image
        hti.screenshot(html_str=htmlString, save_as=f"{pageName}.png")
        #open the image
        image = cv2.imread(f"{pageName}.png")
        #print(htmlString)

        #crop the image to remove any excess empty space at the bottom
        #this allows for seamless merging of images
        # Define the BGR color value for #0E0F13 (the background)
        targetColor = np.array([19, 15, 14])
        # Tolerance for matching the color
        tolerance = 5
        height, width, _ = image.shape
        # Function to check if a row contains the specified color
        def is_color_row(row):
            return np.all(np.abs(row - targetColor) < tolerance, axis=1).all()

        # Find the row where the empty space starts (from the bottom of the image going upwards)
        emptyAreaStart = height
        for row in range(height-1, -1, -1):
            if is_color_row(image[row, :]):
                emptyAreaStart = row
            else:
                break

        # Crop the image above the space
        image = image[:emptyAreaStart, :]

        pageImages.append(image)

    imgOut = cv2.vconcat(pageImages) 
    #Get the original dimensions
    height, width = imgOut.shape[:2]
    # Resize the image
    imgOut = cv2.resize(imgOut, (width*2, height*2))
    cv2.imwrite("hourlyReport.png", imgOut) 
    return hourlyReportData