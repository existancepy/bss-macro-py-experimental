from modules.screen.imageSearch import templateMatch
import cv2

target = cv2.imread("./images/blue/mondo-retina.png")
screen = cv2.imread("rizz.png")

print(templateMatch(target, screen))