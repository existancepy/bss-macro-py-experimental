def jump(self):
    self.keyboard.keyDown("w")
    self.keyboard.slowPress('space')
    sleep(0.25)
    self.keyboard.keyUp("w")

exec(open("../settings/paths/cannon_to_field/mountain top.py").read())
for _ in range(4):
    self.keyboard.press(",")
self.keyboard.walk("w",1)
self.keyboard.slowPress(".")
self.keyboard.walk("w",3)
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.walk("w",6)
self.keyboard.slowPress(".")
self.keyboard.slowPress(".")
self.keyboard.walk("d",0.5)
self.keyboard.walk("w",8)
jump(self)
self.keyboard.walk("w",5)
jump(self)
self.keyboard.walk("w",3)
self.keyboard.walk("s",0.5)

    
