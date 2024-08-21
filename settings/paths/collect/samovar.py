def jump(self):
    self.keyboard.keyDown("w")
    self.keyboard.slowPress('space')
    sleep(0.25)
    self.keyboard.keyUp("w")

exec(open("../settings/paths/cannon_to_field/stump.py").read())
self.keyboard.walk("w",5)
jump(self)
self.keyboard.walk("w",5)
self.keyboard.press(',')
jump(self)
self.keyboard.press('.')
self.keyboard.press('.')
jump(self)

    
