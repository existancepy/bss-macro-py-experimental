def jump(self):
    self.keyboard.keyDown("w")
    self.keyboard.slowPress('space')
    sleep(0.23)
    self.keyboard.keyUp("w")

exec(open("../settings/paths/cannon_to_field/stump.py").read())
self.keyboard.press(',')
self.keyboard.press(',')
self.keyboard.walk("w",5)
jump(self)
self.keyboard.walk("w",4)
self.keyboard.press(',')
jump(self)
self.keyboard.press('.')
self.keyboard.press('.')
jump(self)

    
