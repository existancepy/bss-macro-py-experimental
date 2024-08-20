print("hey")
eggPosData = {
    "basic": -95, 
    "silver": -40,
    "gold": 15,
    "diamond": 70,
    "mythic": 125
}
#click egg
eggPos = eggPosData[self.setdat["sticker_printer_egg"]]
mouse.moveTo(self.mw//2+eggPos, 4*self.mh//10-20)
time.sleep(0.2)
mouse.click()
time.sleep(0.2)
#confirm
mouse.moveTo(self.mw//2+225, 4*self.mh//10+195)
time.sleep(0.1)
mouse.click()
time.sleep(0.2)
self.clickYes()
time.sleep(6)
self.logger.webhook(f"", "Claimed sticker", "light green", "sticker")
#close the inventory
time.sleep(1)
self.toggleInventory()
self.keyboard.press("\\")
