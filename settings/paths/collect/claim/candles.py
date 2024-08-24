sideTime = 0.2
frontTime = 0.55
#self.keyboard.slowPress(",")
self.keyboard.walk('w',0.3)
self.keyboard.walk('a',0.3)
for i in range(3):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("d", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("d", sideTime)

   

    
