from modules.screen.screenshot import mssScreenshot
import pyautogui as pag
screen = mssScreenshot()
screen.save("sigma.png")