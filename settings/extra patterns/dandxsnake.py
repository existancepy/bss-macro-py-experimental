if sizeword.lower() == "xs":
    size = 0.5
elif sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "l":
    size = 2
elif sizeword.lower() == "xl":
    size = 2.5
else:
    size = 1.5
leftkey = tclrkey
rightkey = afclrkey
backkey = afcfbkey
fwdkey = tcfbkey
wm = 0.5*size
sm = 0.25*size
df = (((wm*2)**2)+((sm*4)**2))**0.5
self.keyboard.press(".")
self.keyboard.press("shift")
self.keyboard.press(".")
self.keyboard.walk(leftkey,sm*3)
self.keyboard.walk(backkey,1)
self.keyboard.press(",")
self.keyboard.press("shift")
self.keyboard.press(",")
self.keyboard.walk(leftkey,wm*2.1)
self.keyboard.walk(rightkey,wm)
self.keyboard.multiWalk(["s","d"], df*size)
self.keyboard.walk(fwdkey,sm*6.8)
self.keyboard.walk(backkey,sm*4.5)
self.keyboard.walk(leftkey,wm*2.5)
for i in range(2):
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(leftkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(leftkey,wm*2)
self.keyboard.walk(fwdkey,sm)
self.keyboard.walk(rightkey,wm*2)
self.keyboard.walk(fwdkey,sm)
self.keyboard.walk(leftkey,wm*2)
for i in range(2):
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(leftkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(leftkey,wm*2)
self.keyboard.walk(fwdkey,sm)
for i in range(2):
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(leftkey,wm*2)
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(backkey,sm)
    self.keyboard.walk(leftkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(leftkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(rightkey,wm*2)
    self.keyboard.walk(fwdkey,sm)
    self.keyboard.walk(leftkey,wm*2)
time.sleep(0.08)

