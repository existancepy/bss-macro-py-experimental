sideTime = 0.15
frontTime = 0.5
time.sleep(2.5)
self.keyboard.press(".") #feast messes up the camera angle
self.keyboard.walk('a',0.55)
self.keyboard.walk('w',0.2)
for i in range(2):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("d", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("d", sideTime)
for i in range(2):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("a", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("a", sideTime)
   

    
