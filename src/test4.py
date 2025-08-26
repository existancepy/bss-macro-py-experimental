from modules.screen.imageSearch import templateMatch
import cv2

screen = cv2.imread("screenshot.png")
questTitle = cv2.imread("./images/quest/riley bee-retina.png")
print(templateMatch(questTitle, screen))
