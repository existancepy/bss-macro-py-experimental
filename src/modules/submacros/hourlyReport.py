from html2image import Html2Image
from pathlib import Path
from PIL import Image
import cv2
from modules.misc.settingsManager import readSettingsFile
import math
import time
import ast
hti = Html2Image(size=(1900, 770))

def millify(n):
    if not n: return "0"
    millnames = ['',' K',' M',' B',' T', 'Qd']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

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

        #calculate honey/min
        honeyPerMin = [0]
        prevHoney = hourlyReportData["honey_per_min"][0]
        for x in hourlyReportData["honey_per_min"][1:]:
            honeyPerMin.append(x-prevHoney)
            prevHoney = x

        #replace the contents of the html
        replaceDict = {
            'src="a': f'src="{hourlyReportDir}/a',
            '`as': '`{}/as'.format(str(hourlyReportDir).replace("\\", "/")),
            "-honey": millify(hourlyReportData["honey_per_min"][-1] - hourlyReportData["honey_per_min"][0]),
            "-bugs": hourlyReportData["bugs"],
            "-quests": hourlyReportData["quests_completed"],
            "-vicBees": hourlyReportData["vicious_bees"],
            "-currHoney": millify(hourlyReportData["honey_per_min"][-1]),
            "-sessHoney": millify(hourlyReportData["honey_per_min"][-1]- hourlyReportData["honey_per_min"][0]),
            "-sessTime": display_time(time.time()-hourlyReportData["start_time"], ['d','h','m']),
            "var honeyPerMin = []": f'var honeyPerMin = {honeyPerMin}',
            "var backpackPerMin = []": f'var backpackPerMin = {hourlyReportData["backpack_per_min"]}',
            "const taskTimes = []": f'const taskTimes = [{hourlyReportData["gathering_time"]}, {hourlyReportData["converting_time"]}, {hourlyReportData["bug_run_time"]}, {hourlyReportData["misc_time"]}]',
        }

        if planterData:
            planterData = ast.literal_eval(planterData)
            print("hi")
            planterReplaceDict = {
                "const planterNames = []": f'const planterNames = {planterData["planters"]}', 
                "const planterTimes = []": f'const planterTimes = {[planterData["harvestTime"]-time.time()]*3}',
                "const planterFields = []": f'const planterFields = {planterData["fields"]}',
            }
            replaceDict = {**replaceDict, **planterReplaceDict}
        for k,v in replaceDict.items():
            htmlString = htmlString.replace(k,str(v))
        #save the html as an image
        if "2" in page: print(htmlString)
        hti.screenshot(html_str=htmlString, save_as=f"{pageName}.png")
        #open the image in pillow
        pageImages.append(cv2.imread(f"{pageName}.png"))

    imgOut = cv2.vconcat(pageImages) 
    #Get the original dimensions
    height, width = imgOut.shape[:2]
    # Resize the image
    imgOut = cv2.resize(imgOut, (width*2, height*2))
    cv2.imwrite("hourlyReport.png", imgOut) 