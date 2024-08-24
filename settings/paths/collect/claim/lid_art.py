time.sleep(1)
sideTime = 0.2
frontTime = 0.4
self.keyboard.walk('w',0.2)
self.keyboard.walk('d',0.6)
for i in range(3):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("a", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("a", sideTime)
for i in range(3):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("d", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("d", sideTime)
   

    
