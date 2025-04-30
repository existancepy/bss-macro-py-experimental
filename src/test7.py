import math
import random
import os
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import time

class HourlyReportDrawer:
    def __init__(self):
        self.backgroundColor = "#0E0F13"
        self.canvasSize = (6400, 9000)
        self.sidebarWidth = 1900
        self.leftPadding = 150
        self.availableSpace = self.canvasSize[0] - self.sidebarWidth - self.leftPadding*2
        self.bodyColor = "#FFFFFF"
        self.hour = datetime.now().hour
        self.sideBarBackground = (23, 25, 29)
        if self.hour == 0:
            self.hour = 23
        else:
            self.hour -= 1
        self.assetPath = "hourly_report/assets"

    def transformXLabelTime(self, i, val):
        if i%10:
            return
        hour = self.hour
        if val == 60:
            hour += 1
            if hour == 24:
                hour = 0
            val = 0
        return f"{str(hour).zfill(2)}:{str(val).zfill(2)}"

    def millify(self, n):
        if not n: return "0"
        millnames = ['',' K',' M',' B',' T', 'Qd']
        n = float(n)
        millidx = max(0,min(len(millnames)-1,
                            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

        return '{:.2f} {}'.format(n / 10**(3 * millidx), millnames[millidx])

    def displayTime(self, seconds, units = ['w','d','h','m','s']):
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
        return ' '.join(result)
        
    def getFont(self, weight, fontSize):
        return ImageFont.truetype(f"hourly_report/Inter/static/Inter_18pt-{weight.title()}.ttf", fontSize)

    def getGradientColorAtRatio(self, ratio, gradientSpec):
        #calculates the RGBA color from gradientSpec at a given vertical ratio (0=bottom, 1=top)
        if not gradientSpec:
            return (0, 0, 0, 0) # Default transparent black if no spec

        sorted_stops = sorted(gradientSpec.items()) # list of (position_ratio, color_tuple)

        # Clamp ratio
        ratio = max(0.0, min(1.0, ratio))

        # Find which two stops this ratio is between
        for j in range(len(sorted_stops) - 1):
            pos1, col1 = sorted_stops[j]
            pos2, col2 = sorted_stops[j + 1]
            if pos1 <= ratio <= pos2:
                if pos2 - pos1 == 0:
                    local_ratio = 0
                else:
                    local_ratio = (ratio - pos1) / (pos2 - pos1)

                #interpolate RGBA values
                try:
                    r = int(col1[0] + (col2[0] - col1[0]) * local_ratio)
                    g = int(col1[1] + (col2[1] - col1[1]) * local_ratio)
                    b = int(col1[2] + (col2[2] - col1[2]) * local_ratio)
                    #handle alpha
                    a = 255 
                    if len(col1) > 3 and len(col2) > 3:
                            a = int(col1[3] + (col2[3] - col1[3]) * local_ratio)
                    elif len(col1) > 3:
                        a = col1[3]
                    elif len(col2) > 3:
                        a = col2[3]

                    return (r, g, b, a)
                except IndexError:
                    print(f"Warning: Color tuple length mismatch in gradientSpec between {col1} and {col2}")
                    return (0,0,0,255)

        # If ratio is below the first stop or above the last stop (should not happen with clamping)
        if ratio < sorted_stops[0][0]:
            return sorted_stops[0][1] # Return first color
        else:
            return sorted_stops[-1][1] # Return last color


    def drawGraph(self, graphX, graphY, width, height, xData, datasets, maxY = None, showXAxisLabels=True, showYAxisLabels=True, ticks=5, yLabelFunc=None, xLabelFunc=None):
        # Validate data lengths
        for dataset in datasets:
            data = dataset["data"]
            #pad the data
            data = [0]*(len(xData) - len(data)) + data
        
            xInterval = width / (len(data) - 1)
            if not maxY:
                maxY = max(data)

            font = self.getFont("semibold", 60)
            fontColor = (175, 175, 175)
            gridColor = (65, 65, 65)
            #draw xaxis
            if showXAxisLabels:
                for i, val in enumerate(xData):
                    val = xLabelFunc(i, val) if xLabelFunc else val
                    if val:
                        val = str(val)
                        #get the text width, so the text can be centered with the x axis point
                        bbox = self.draw.textbbox((0, 0), val, font=font)
                        textWidth = bbox[2] - bbox[0]
                        self.draw.text((graphX+xInterval*i - textWidth/2, graphY+20), val, font=font, fill= fontColor)
            
            #draw y labels and y grid
            #calculating ticks
            yInterval = height/(ticks-1)
            yValInterval = maxY/(ticks-1)

            yLabels = []
            for i in range(ticks):
                y = graphY - yInterval*i
                if showYAxisLabels:
                    text = yValInterval*i
                    text = yLabelFunc(i, text) if yLabelFunc else text
                    if text:
                        text = str(text)
                        bbox = self.draw.textbbox((0, 0), text, font=font)
                        textWidth = bbox[2] - bbox[0]
                        textHeight = bbox[3] - bbox[1]
                        self.draw.text((graphX - textWidth - 100, y - textHeight/2), text, font=font, fill= fontColor)
                self.draw.line((graphX-30, y, graphX+30+width, y), fill=gridColor, width=3)


            # Collect curve points
            points = []
            for i, val in enumerate(data):
                px = graphX + i * xInterval
                py = graphY - (val / maxY * height)
                points.append((px, py))
            # Close polygon at bottom
            points.append((graphX + (len(xData) - 1) * xInterval, graphY))
            points.append((graphX, graphY))

            #make gradient
            gradientSpec = dataset.get("gradientFill", None)
            if gradientSpec:
                gradient = Image.new('RGBA', (int(width), int(height)), (0, 0, 0, 0))
                grad_draw = ImageDraw.Draw(gradient)
                sorted_stops = sorted(gradientSpec.items())  # list of (position, color)
                stop_positions = [int(pos * height) for pos, _ in sorted_stops]

                for i in range(height):
                    # Normalize position (0 to 1)
                    ratio = i / float(height - 1)

                    # Find which two stops this ratio is between
                    for j in range(len(sorted_stops) - 1):
                        pos1, col1 = sorted_stops[j]
                        pos2, col2 = sorted_stops[j + 1]
                        if pos1 <= ratio <= pos2:
                            local_ratio = (ratio - pos1) / (pos2 - pos1)
                            r = int(col1[0] + (col2[0] - col1[0]) * local_ratio)
                            g = int(col1[1] + (col2[1] - col1[1]) * local_ratio)
                            b = int(col1[2] + (col2[2] - col1[2]) * local_ratio)
                            a = int(col1[3] + (col2[3] - col1[3]) * local_ratio)
                            grad_draw.line([(0, height - i), (width, height - i)], fill=(r, g, b, a))
                            break
                

            #composite gradient on dark background
            bg = Image.new('RGBA', (int(width), int(height)), self.backgroundColor)
            gradient = Image.alpha_composite(bg, gradient)

            #create a mask with polygon in the shape of the graph
            mask = Image.new('L', (int(width), int(height)), 0)
            mask_draw = ImageDraw.Draw(mask)
            rel_pts = [(px - graphX, py - (graphY - height)) for px, py in points]
            mask_draw.polygon(rel_pts, fill=255)

            #paste the gradient and mask onto the canvas
            self.canvas.paste(gradient, (graphX, graphY - height), mask)

            lineColor = dataset["lineColor"]
            #gradient color.
            if gradientSpec and lineColor == "gradient":
                #draw the line
                for i in range(len(points) - 3):
                    #Since line doesnt accept gradients, we will break the line down into segments, 
                    #and assign each segment a color
                    x0, y0 = points[i]
                    x1, y1 = points[i+1]

                    #calculate length of the line
                    dx = x1 - x0
                    dy = y1 - y0
                    length = math.sqrt(dx*dx + dy*dy)

                    if length == 0: continue # Skip zero-length segments

                    #get the number of segments
                    segmentCount = max(1, int(length / 10))

                    for k in range(segmentCount):
                        t0 = k / segmentCount
                        t1 = (k + 1) / segmentCount

                        sub_x0 = x0 + dx * t0
                        sub_y0 = y0 + dy * t0
                        sub_x1 = x0 + dx * t1
                        sub_y1 = y0 + dy * t1
                        mid_y = (sub_y0 + sub_y1) / 2.0
                        # Convert Y coord to ratio (0=bottom, 1=top)
                        mid_yRatio = (graphY - mid_y) / height if height > 0 else 0.0

                        # Get color for this ratio
                        r, g, b, a = self.getGradientColorAtRatio(mid_yRatio, gradientSpec)

                        self.draw.line(
                            (int(sub_x0), int(sub_y0), int(sub_x1), int(sub_y1)),
                            fill=(r, g, b), # Use opaque RGB for line
                            width=7
                        )

            else:
                # Draw the entire line with a solid color
                # Use points[:len(data)] to only draw line over actual data points, not polygon closing points
                self.draw.line(points[:len(data)], fill=lineColor, width=7)

    def drawDoughnutChart(self, x, y, size, datasets, holeRatio = 0.6):

        total = sum([x["data"] for x in datasets])
        angleStart = -90
        chartArea = (x, y, x+size, y+size)

        #draw the section
        for dataset in datasets:
            angleEnd = angleStart + (dataset["data"] / total) * 360
            self.draw.pieslice(chartArea, angleStart, angleEnd, fill=dataset["color"])
            angleStart = angleEnd

        #draw the hole
        if holeRatio > 0:
            hole_size = int(size * holeRatio)
            offset = (size - hole_size) // 2
            hole_bbox = (x+offset, y+offset, x+offset + hole_size, y+offset + hole_size)
            self.draw.ellipse(hole_bbox, fill=self.backgroundColor)
    
    def drawProgressChart(self, x, y, size, percentage, color, holeRatio = 0.6,):
        chartArea = (x, y, x+size, y+size)

        #draw the section
        self.draw.pieslice(chartArea, -90, 360, fill=(*color, 140))
        self.draw.pieslice(chartArea, -90, (percentage / 100) * 360 - 90, fill=color)

        #draw the hole
        if holeRatio > 0:
            hole_size = int(size * holeRatio)
            offset = (size - hole_size) // 2
            hole_bbox = (x+offset, y+offset, x+offset + hole_size, y+offset + hole_size)
            self.draw.ellipse(hole_bbox, fill=self.backgroundColor)

        font = self.getFont("semibold", 65)
        text = f"{percentage}%"
        text_bbox = self.draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        self.draw.text((x + (size - text_width) // 2, y + (size - text_height) // 2 - 10), text, fill=self.bodyColor, font=font)
    
    def drawStatCard(self, x, y, statImage, statValue, statTitle, fontColor = None, imageColor = None):
        leftPadding = x+100
        self.draw.rounded_rectangle((x,y, x+700, y+750), fill=(int(23*1.2), int(25*1.2), int(29*1.2)), radius=60)
        #load the image 
        img = Image.open(f"{self.assetPath}/{statImage}.png").convert("RGBA")
        width, height = img.size
        imageHeight = 200
        imageWidth = int(width*(imageHeight/height))
        img = img.resize((imageWidth, imageHeight))
        
        #recolor the image
        if imageColor:
            r,g,b = imageColor
            pixels = img.load()
            for i in range(img.width):
                for j in range(img.height):
                    _, _, _, a = pixels[i, j]
                    if a > 0:  #only recolor non-transparent pixels
                        pixels[i, j] = (r,g,b, a)

        self.canvas.paste(img, (leftPadding, y + 100), img)

        self.draw.text((leftPadding, y+380), str(statValue), font=self.getFont("semibold", 80), fill=fontColor if fontColor else self.bodyColor)
        self.draw.text((leftPadding, y+550), statTitle, font=self.getFont("medium", 55), fill=self.bodyColor)
    
    def drawBuffUptimeGraphStackableBuff(self, y, datasets, imageName, ):
        #draw the graph
        graphHeight = 550
        graphXStart = self.leftPadding+450
        xData = list(range(601))
        self.drawGraph(graphXStart, y, self.availableSpace-570, graphHeight, xData, datasets, maxY=10, showXAxisLabels=False, showYAxisLabels=False, ticks=3)

        #load the icon
        imageDimension = 200
        imageX = graphXStart - 200 - imageDimension
        imageY = y - graphHeight//2 - imageDimension//2 + len(datasets)*10
        img = Image.open(f"{self.assetPath}/{imageName}.png").convert("RGBA")
        img = img.resize((imageDimension, imageDimension))
        self.canvas.paste(img, (imageX, imageY), img)

        self.draw.text((imageX, imageY + imageDimension+15), "x0-10", font=self.getFont("semibold", 70), fill=self.bodyColor)

        for i, dataset in enumerate(datasets):
            self.draw.text((imageX+20, imageY - (90+60*i)), dataset["average"], font=self.getFont("semibold", 60), fill=dataset["lineColor"])
    
    def drawSessionStat(self, y, imageName, label, value, valueColor):
        imgContainerDimension = 180
        self.draw.rounded_rectangle((self.sidebarX, y, self.sidebarX+imgContainerDimension, y+imgContainerDimension), radius=50, fill=(int(45*1.1), int(46*1.1), int(53*1.1)))
        img = Image.open(f"{self.assetPath}/{imageName}.png").convert("RGBA")
        width, height = img.size
        imageWidth = 120
        imageHeight = int(height*(imageWidth/width))
        img = img.resize((imageWidth, imageHeight))
        #center the image in the container
        self.canvas.paste(img, (self.sidebarX + (imgContainerDimension-imageWidth)//2 , y + (imgContainerDimension-imageHeight)//2), img)

        #draw label and value
        #make sure they are vertically centered with the image container
        font = self.getFont("semibold", 68)
        ascent, _ = font.getmetrics()
        textY = y + (imgContainerDimension - ascent)//2
        self.draw.text((self.sidebarX+imgContainerDimension+50, textY), label, self.bodyColor, font=font)
        #value is right-aligned
        bbox = self.draw.textbbox((0, 0), value, font=font)
        textWidth = bbox[2] - bbox[0]
        self.draw.text((self.canvasSize[0]-self.sidebarPadding-textWidth, textY), str(value), valueColor, font=font)

    def drawTaskTimes(self, y, datasets):
        legendIconDimension = 80
        font = self.getFont("medium", 68)
        x = self.sidebarX
        totalData = sum([x["data"] for x in datasets])
        for dataset in datasets:
            self.draw.rounded_rectangle((x, y, x+legendIconDimension, y+legendIconDimension), fill=dataset["color"], radius=10)
            bbox = self.draw.textbbox((0, 0), dataset["label"], font=font)
            textHeight = bbox[3] - bbox[1]
            textY = y #+ (legendIconDimension - textHeight) // 2 -25
            self.draw.text((x+legendIconDimension + 50, textY), f"{dataset['label']}:", self.bodyColor, font=font)
            self.draw.text((x+legendIconDimension + 600, textY), self.displayTime(dataset["data"]), self.bodyColor, font=font)
            self.draw.text((x+legendIconDimension + 1000, textY), f"{round(dataset['data']/totalData*100, 1)}%", (220,220,220), font=font)
            y+= 150

        y += 100
        doughnutChartSize = 600
        self.drawDoughnutChart(self.sidebarX + 450, y, doughnutChartSize, datasets, holeRatio=0.4)
    
    def drawPlanters(self, y, planterNames, planterTimes, planterFields):
        fieldNectarIcons = {
            "sunflower": "satisfying",
            "dandelion": "comforting",
            "mushroom": "motivating",
            "blue flower": "refreshing",
            "clover": "invigorating",
            "strawberry": "refreshing",
            "spider": "motivating",
            "bamboo": "comforting",
            "pineapple": "satisfying",
            "stump": "motivating",
            "cactus": "invigorating",
            "pumpkin": "satisfying",
            "pine tree": "comforting",
            "rose": "motivating",
            "mountain top": "invigorating",
            "pepper": "invigorating",
            "coconut": "refreshing"
        }

        planterX = self.sidebarX
        fieldFont = self.getFont("semibold", 68)
        timeFont = self.getFont("semibold", 55)
        for i in range(len(planterNames)):
            bbox = self.draw.textbbox((0, 0), planterFields[i].title(), font=fieldFont)
            fieldTextWidth = bbox[2] - bbox[0]

            nectarImg = Image.open(f'{self.assetPath}/{fieldNectarIcons[planterFields[i]]}.png')
            width, height = nectarImg.size
            nectarImageHeight = bbox[3] - bbox[1]
            nectarImageWidth = int(width*(nectarImageHeight/height))
            nectarImg = nectarImg.resize((nectarImageWidth, nectarImageHeight))

            fieldAndNectarWidth = fieldTextWidth + nectarImageWidth + 30

            img = Image.open(f'{self.assetPath}/{planterNames[i].replace(" ","_")}_planter.png')
            width, height = img.size
            imageHeight = 250
            imageWidth = int(width*(imageHeight/height))
            img = img.resize((imageWidth, imageHeight))

            timeText = self.displayTime(planterTimes[i], ["m", "s"])
            bbox = self.draw.textbbox((0, 0), timeText, font=timeFont)
            timeTextWidth = bbox[2] - bbox[0]

            maxWidth = max(fieldAndNectarWidth, imageWidth, timeTextWidth)
            self.canvas.paste(img, (planterX + (maxWidth-imageWidth)//2, y), img)
            self.draw.text((planterX + (maxWidth - fieldAndNectarWidth)//2, y+300), planterFields[i].title(), font=fieldFont, fill= self.bodyColor) 
            self.canvas.paste(nectarImg, (planterX + (maxWidth - fieldAndNectarWidth)//2 + fieldTextWidth + 30, y+315), nectarImg)
            self.draw.text((planterX + (maxWidth - timeTextWidth)//2, y+400), timeText, font=timeFont, fill= tuple([180]*3)) 

            planterX += maxWidth + 200
    
    def drawBuffs(self, y, buffData):
        buffImages = ["tabby_love_buff", "polar_power_buff", "wealth_clock_buff", "blessing_buff", "bloat_buff"]

        font = self.getFont("bold", 68)
        for i in range(len(buffData)):
            buff = str(buffData[i]) #I cant make up my mind on if buffData should switch to ints or remain as string
            x = self.sidebarX + 340*i

            img = Image.open(f"{self.assetPath}/{buffImages[i]}.png").convert("RGBA")
            width, height = img.size
            imageWidth = 250
            imageHeight= int(width*(imageWidth/height))
            img = img.resize((imageWidth, imageHeight))

            if buff == "0":
                #dim the image
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 100))
            else:
                overlay = Image.new("RGBA", img.size, (0, 0, 0, 20))
            img = Image.alpha_composite(img, overlay)
            self.canvas.paste(img, (x, y), img)

            if buff != "0":
                buffText = f"x{buff}"
                bbox = self.draw.textbbox((0, 0), buffText, font=font, stroke_width=4)
                textWidth = bbox[2] - bbox[0]
                textHeight = 68
                self.draw.text((x + imageWidth - textWidth - 5, y + imageHeight - textHeight - 20), buffText, fill=self.bodyColor, font=font, stroke_width=4, stroke_fill=(0,0,0))

    def drawNectars(self, y, nectarData):
        nectarColors = [(165, 207, 234), (235, 120, 108), (194, 166, 236), (162, 239, 163), (239, 205, 224)]
        nectarNames = ["comforting", "invigorating", "motivating", "refreshing", "satisfying"]
        progressChartSize = 300
        imageHeight = 120
        for i in range(len(nectarData)):
            x = self.sidebarX + i*(progressChartSize+50)
            self.drawProgressChart(x, y, progressChartSize, nectarData[i], nectarColors[i], 0.75)

            img = Image.open(f"{self.assetPath}/{nectarNames[i]}.png").convert("RGBA")
            width, height = img.size
            imageWidth = int(width*(imageHeight/height))
            img = img.resize((imageWidth, imageHeight))
            self.canvas.paste(img, (x + (progressChartSize-imageWidth)//2, y+progressChartSize + 80), img)

    def drawHourlyReport(self, hourlyReportStats, sessionTime, honeyPerMin, sessionHoney, honeyThisHour, onlyValidHourlyHoney, buffQuantity, nectarQuantity, planterData, uptimeBuffsValues, buffGatherIntervals):

        def getAverageBuff(self, buffValues):
            #get the buff average when gathering, rounded to 2p
            count = 0
            total = 0
            for i, e in enumerate(self.buffGatherIntervals):
                if e:
                    total += buffValues[i]
                    count += 1

            res = total/count if count else 0
                
            return f"x{res:.2f}"
    
        self.canvas = Image.new('RGBA', self.canvasSize, self.backgroundColor)
        self.draw = ImageDraw.Draw(self.canvas)

        mins = list(range(61))

        #draw aside bar
        self.draw.rectangle((self.canvasSize[0]-self.sidebarWidth, 0, self.canvasSize[0], self.canvasSize[1]), fill=self.sideBarBackground)

        #draw icon
        macroIcon = Image.open(f"{self.assetPath}/macro_icon.png")
        # macroIcon = macroIcon.resize((170, 170))
        self.canvas.paste(macroIcon, (5550, 100), macroIcon)
        self.draw.text((5750, 120), "Existance Macro", fill=self.bodyColor, font=self.getFont("semibold", 70))

        #draw title
        self.draw.text((self.leftPadding, 80), "Hourly Report", fill=self.bodyColor, font=self.getFont("bold", 120))
        self.draw.text((self.leftPadding, 260), "Your stats for this hour", fill=self.bodyColor, font=self.getFont("medium", 60))

        #section 1: hourly stats
        y = 470
        statSpacing = (self.availableSpace+self.leftPadding)//5
        self.drawStatCard(self.leftPadding, y, "average_icon", self.millify(sessionHoney/(sessionTime/3600)), "Average Honey\nPer Hour")
        self.drawStatCard(self.leftPadding+statSpacing*1, y, "honey_icon", self.millify(honeyThisHour), "Honey Made\nThis Hour", (248,191,23))
        self.drawStatCard(self.leftPadding+statSpacing*2, y, "kill_icon", hourlyReportStats["bugs"], "Bugs Killed\nThis Hour", (254,101,99), (254,101,99))
        self.drawStatCard(self.leftPadding+statSpacing*3, y, "quest_icon", hourlyReportStats["quests_completed"], "Quests Completed\nThis Hour", (103,253,153), (103,253,153))
        self.drawStatCard(self.leftPadding+statSpacing*4, y, "vicious_bee_icon", hourlyReportStats["vicious_bees"], "Vicious Bees\nThis Hour", (132,233,254), (132,233,254))

        #section 2: honey/min
        y += 900
        self.draw.text((self.leftPadding, y), "Honey/Sec", fill=self.bodyColor, font=self.getFont("semibold", 85))
        y += 950
        dataset = [{
            "data": honeyPerMin,
            "lineColor": (174, 22, 250),
            "gradientFill": {
                0: (174,22,250,38),
                1: (174,22,250,153)
            }
        }]
        self.drawGraph(self.leftPadding+450, y, self.availableSpace-570, 700, mins, dataset, xLabelFunc= self.transformXLabelTime, yLabelFunc=lambda i,x : self.millify(x))

        #section 3: backpack
        y += 200
        self.draw.text((self.leftPadding, y), "Backpack", fill=self.bodyColor, font=self.getFont("semibold", 85))
        y += 950
        dataset = [{
            "data": hourlyReportStats["backpack_per_min"],
            "lineColor": "gradient",
            "gradientFill": {
                0: (65, 255, 128, 90),
                0.6: (201, 163, 36, 90),
                0.9: (255, 65, 84, 90),
                1: (255, 65, 84, 90),
            }
        }]
        self.drawGraph(self.leftPadding+450, y, self.availableSpace-570, 700, mins, dataset, maxY=100, xLabelFunc= self.transformXLabelTime)

        #section 4: buff uptime
        y += 200
        self.draw.text((self.leftPadding, y), "Buff Uptime", fill=self.bodyColor, font=self.getFont("semibold", 85))
        y += 750
        dataset = [
        {
            "data": uptimeBuffsValues["blue_boost"],
            "lineColor": (77,147,193),
            "average": getAverageBuff(uptimeBuffsValues["blue_boost"]),
            "gradientFill": {
                0: (77,147,193,10),
                1: (77,147,193,120),
            }
        },
        {
            "data": uptimeBuffsValues["red_boost"],
            "lineColor": (200,90,80),
            "average": getAverageBuff(uptimeBuffsValues["red_boost"]),
            "gradientFill": {
                0: (200,90,80,10),
                1: (200,90,80,120),
            }
        },
        {
            "data": uptimeBuffsValues["white_boost"],
            "lineColor": (220,220,220),
            "average": getAverageBuff(uptimeBuffsValues["white_boost"]),
            "gradientFill": {
                0: (220,220,220,10),
                1: (220,220,220,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "boost_buff")

        y += 560
        dataset = [
        {
            "data": uptimeBuffsValues["haste"],
            "lineColor": (210,210,210),
            "average": getAverageBuff(uptimeBuffsValues["haste"]),
            "gradientFill": {
                0: (210,210,210,10),
                1: (210,210,210,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "haste_buff")

        y += 560
        dataset = [
        {
            "data": uptimeBuffsValues["focus"],
            "lineColor": (30,191,5),
            "average": getAverageBuff(uptimeBuffsValues["focus"]),
            "gradientFill": {
                0: (30,191,5,10),
                1: (30,191,5,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "focus_buff")

        y += 560
        dataset = [
        {
            "data": uptimeBuffsValues["bomb_combo"],
            "lineColor": (160,160,160),
            "average": getAverageBuff(uptimeBuffsValues["bomb_combo"]),
            "gradientFill": {
                0: (160,160,160,10),
                1: (160,160,160,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "bomb_combo_buff")

        y += 560
        dataset = [
        {
            "data": uptimeBuffsValues["balloon_aura"],
            "lineColor": (50,80,200),
            "average": getAverageBuff(uptimeBuffsValues["balloon_aura"]),
            "gradientFill": {
                0: (50,80,200,10),
                1: (50,80,200,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "balloon_aura_buff")

        y += 560
        dataset = [
        {
            "data": uptimeBuffsValues["inspire"],
            "lineColor": (195,191,18),
            "average": getAverageBuff(uptimeBuffsValues["inspire"]),
            "gradientFill": {
                0: (195,191,18,10),
                1: (195,191,18,120),
            }
        }
        ]
        self.drawBuffUptimeGraphStackableBuff(y, dataset, "inspire_buff")

        #side bar 

        #session stats

        y2 = 470
        self.sidebarPadding = 110
        self.sidebarX = self.canvasSize[0] - self.sidebarWidth + self.sidebarPadding
        self.draw.text((self.sidebarX, y2), "Session", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawSessionStat(y2, "time_icon", "Session Time", self.displayTime(sessionTime, ['d','h','m']), self.bodyColor)
        y2 += 300
        self.drawSessionStat(y2, "honey_icon", "Current Honey", self.millify(onlyValidHourlyHoney[-1]), "#F8BF17")
        y2 += 300
        self.drawSessionStat(y2, "session_honey_icon", "Session Honey", self.millify(sessionHoney), "#FDE395")

        #task times
        y2 += 500
        self.draw.text((self.sidebarX, y2), "Task Times", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawTaskTimes(y2, [
            {
                "label": "Gathering",
                "data": hourlyReportStats["gathering_time"],
                "color": "#6A0DAD"
            },
            {
                "label": "Converting",
                "data": hourlyReportStats["converting_time"],
                "color": "#9966FF"
            },
            {
                "label": "Bug Run",
                "data": hourlyReportStats["bug_run_time"],
                "color": "#C3A6FF"
            },
            {
                "label": "Misc",
                "data": hourlyReportStats["misc_time"],
                "color": "#E6D6FF"
            },
            

        ])

        #planters
        y2 += 1500
        planterNames = planterData["planters"]
        #check if there are planters
        if planterNames:
            planterTimes = [planterData["harvestTime"]-time.time()]*3
            planterFields = planterData["fields"]
            if planterNames:
                self.draw.text((self.sidebarX, y2), "Planters", font=self.getFont("semibold", 85), fill=self.bodyColor)
                y2 += 250
                self.drawPlanters(y2, planterNames, planterTimes, planterFields)
        
        #buffs
        y2 += 650
        self.draw.text((self.sidebarX, y2), "Buffs", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawBuffs(y2, buffQuantity)

        #nectars
        y2 += 500
        self.draw.text((self.sidebarX, y2), "Nectars", font=self.getFont("semibold", 85), fill=self.bodyColor)
        y2 += 250
        self.drawNectars(y2, nectarQuantity)
    
