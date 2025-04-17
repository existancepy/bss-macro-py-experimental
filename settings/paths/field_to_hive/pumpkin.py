hiveNumber = self.setdat["hive_number"]

self.keyboard.walk("s",6)
self.keyboard.walk("d",7, False)
self.keyboard.press('space')
self.keyboard.walk("s",6)
self.keyboard.walk("a",14,False)
self.keyboard.walk("w",8, False)
self.keyboard.walk("d",3)
self.keyboard.walk("s",0.5)
self.keyboard.walk("w",1)
self.keyboard.slowPress("space")
time.sleep(0.1)
self.keyboard.walk("w",0.09, False)
time.sleep(1)
self.keyboard.slowPress("space")
time.sleep(0.1)
self.keyboard.slowPress("space")
time.sleep(6)
self.keyboard.walk("w",3)

if hiveNumber >= 3:
    self.keyboard.walk("s",0.5)
else:
    self.keyboard.walk("s",0.4)
    self.keyboard.walk("d",3.2, False)
    self.keyboard.walk("w",0.8)
    self.keyboard.multiWalk(["s","a"], 0.87)
self.keyboard.walk("d",0.25)

    
