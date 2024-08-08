
def acchold(key, duration):
    ws = loadsettings.load()["walkspeed"]
    self.keyboard.keyDown(key)
    sleep(duration*ws/28)
    self.keyboard.keyUp(key)

sideTime = 0
frontTime = 0.45
#self.keyboard.slowPress(",")
acchold('a',0.3)
for i in range(3):
    acchold("w", frontTime)
    acchold("a", sideTime)
    acchold("s", frontTime)
    acchold("d", sideTime)

   

    
