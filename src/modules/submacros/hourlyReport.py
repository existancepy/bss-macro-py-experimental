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
def versionTuple(v):
    return tuple(map(int, (v.split("."))))
macVer = platform.mac_ver()[0]

try:
    hti = Html2Image(size=(1900, 780))
except FileNotFoundError:
    if versionTuple(macVer) >= versionTuple("10.15"):
        msgBox(title = "error", text = "Google Chrome could not be found. Ensure that:\
    \n1. Google Chrome is installed\nGoogle chrome is in the applications folder (open the google chrome dmg file. From the pop up, drag the icon into the folder)")
    else:
        hti = None

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

def generateHourlyReport():
    pages = ["page1.html", "page2.html"]
    pageImages = []
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
        sessionHoney = hourlyReportData["honey_per_min"][-1]- hourlyReportData["start_honey"]
        sessionTime = time.time()-hourlyReportData["start_time"]
        honeyThisHour = hourlyReportData["honey_per_min"][-1] - hourlyReportData["honey_per_min"][0]
        #replace the contents of the html
        replaceDict = {
            'src="a': f'src="{hourlyReportDir}/a',
            '`as': '`{}/as'.format(str(hourlyReportDir).replace("\\", "/")),
            "-avgHoney": millify(sessionHoney/(sessionTime/3600)),
            "-honey": millify(honeyThisHour),
            "-bugs": hourlyReportData["bugs"],
            "-quests": hourlyReportData["quests_completed"],
            "-vicBees": hourlyReportData["vicious_bees"],
            "-currHoney": millify(hourlyReportData["honey_per_min"][-1]),
            "-sessHoney": millify(sessionHoney),
            "-sessTime": display_time(sessionTime, ['d','h','m']),
            "var honeyPerMin = []": f'var honeyPerMin = {honeyPerMin}',
            "var backpackPerMin = []": f'var backpackPerMin = {hourlyReportData["backpack_per_min"]}',
            "const taskTimes = []": f'const taskTimes = [{hourlyReportData["gathering_time"]}, {hourlyReportData["converting_time"]}, {hourlyReportData["bug_run_time"]}, {hourlyReportData["misc_time"]}]',
            "const historyData = []": f'const historyData = {historyData}',
            "const honey = 0": f'const honey = {honeyThisHour}'
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