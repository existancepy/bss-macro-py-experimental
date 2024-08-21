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

exec(open("./paths/field_mountain top.py").read())
for _ in range(4):
    self.keyboard.slowPress(".")
acchold("w",1)
self.keyboard.slowPress(".")
acchold("w",3)
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
acchold("w",6)
self.keyboard.slowPress(".")
self.keyboard.slowPress(".")
acchold("d",0.5)
acchold("w",8)
jump()
acchold("w",5)
jump()
acchold("w",3)
acchold("s",0.5)

    
