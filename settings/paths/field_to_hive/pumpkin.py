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
self.keyboard.walk("s",0.3)
self.keyboard.walk("d",5, False)
self.keyboard.walk("w",1)
self.keyboard.multiWalk(["s","a"], 0.9)
self.keyboard.walk("d",0.25)

    
