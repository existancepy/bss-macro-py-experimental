sideTime = 0.15
frontTime = 0.45
time.sleep(1)
self.keyboard.walk('a',0.55)
self.keyboard.walk('w',0.2)
for i in range(2):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("d", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("d", sideTime)
for i in range(3):
    self.keyboard.walk("s", frontTime)
    self.keyboard.walk("a", sideTime)
    self.keyboard.walk("w", frontTime)
    self.keyboard.walk("a", sideTime)
   

    
