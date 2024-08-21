sideTime = 0
frontTime = 0.45
#self.keyboard.slowPress(",")
self.keyboard.walk('a',0.3)
for i in range(3):
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("a", sideTime)
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("d", sideTime)

   

    
