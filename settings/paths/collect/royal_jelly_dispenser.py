self.keyboard.slowPress(",")
self.keyboard.slowPress("e")
self.keyboard.keyDown("w")
time.sleep(0.12)
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
time.sleep(3.5)
self.keyboard.keyUp("w")
self.keyboard.slowPress("space")
time.sleep(0.5)
self.keyboard.walk("w",3.5)
self.keyboard.walk("d",2.5)
self.keyboard.walk("s",1.5)
    
