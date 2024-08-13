def acchold(key, duration):
    ws = loadsettings.load()["walkspeed"]
    self.keyboard.keyDown(key)
    sleep(duration*ws/28)
    self.keyboard.keyUp(key)
def jump():
    self.keyboard.keyDown("w")
    self.keyboard.slowPress('space')
    sleep(0.25)
    self.keyboard.keyUp("w")

exec(open("./paths/field_stump.py").read())
for _ in range(4):
    self.keyboard.slowPress(',')
acchold("w",5)
jump()
acchold("w",5)
self.keyboard.slowPress(',')
jump()
self.keyboard.slowPress('.')
self.keyboard.slowPress('.')
jump()

    
