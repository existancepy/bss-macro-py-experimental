from mss import mss
import mss.tools as tools

with mss() as sct:
    img = sct.grab_window("Roblox")
    tools.to_png(img.rgb, img.size, output="no.png")