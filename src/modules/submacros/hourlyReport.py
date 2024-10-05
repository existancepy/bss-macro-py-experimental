from html2image import Html2Image
from pathlib import Path
from PIL import Image
import cv2
hti = Html2Image(size=(1900, 770))

def screenshotHTML(path, saveAsName):
    with open(path, "r") as f:
        htmlString = f.read()
    f.close()
    #relative file paths do not work, so replace the paths in src with absolute paths
    hourlyReportDir = Path(__file__).parents[2] / "hourly_report"
    htmlString = htmlString.replace('src="a', f'src="{hourlyReportDir}/a')
    print(htmlString)
    return hti.screenshot(html_str=htmlString, save_as=saveAsName)

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
        #replace the contents of the html
        htmlString = htmlString.replace('src="a', f'src="{hourlyReportDir}/a')
        htmlString = htmlString.replace('`as', '`{}/as'.format(str(hourlyReportDir).replace("\\", "/")))
        #save the html as an image
        print(htmlString)
        hti.screenshot(html_str=htmlString, save_as=f"{pageName}.png")
        #open the image in pillow
        pageImages.append(cv2.imread(f"{pageName}.png"))

    imgOut = cv2.vconcat(pageImages) 
    #Get the original dimensions
    height, width = imgOut.shape[:2]
    # Resize the image
    imgOut = cv2.resize(imgOut, (width*2, height*2))
    cv2.imwrite("hourlyReport.png", imgOut) 