hiveNumber = self.setdat["hive_number"]
self.keyboard.walk("s",5)
self.keyboard.walk("a",1)
self.keyboard.walk("a",10, False)
self.keyboard.walk("w",6.9, False)
self.keyboard.walk("d",1, False)
self.keyboard.press("shift")
self.keyboard.walk("w",0.1, False)
self.keyboard.press("shift")
self.keyboard.slowPress("space")
time.sleep(0.1)
self.keyboard.slowPress("space")
time.sleep(5.5)
self.keyboard.walk("w",1.25, False)

if hiveNumber >= 3:
    self.keyboard.walk("s",0.5)
else:
    self.keyboard.walk("s",0.4)
    self.keyboard.walk("d",3.2, False)
    self.keyboard.walk("w",0.8)
    self.keyboard.multiWalk(["s","a"], 0.87)
self.keyboard.walk("d",0.25)

    
