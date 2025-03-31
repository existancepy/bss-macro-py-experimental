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

self.keyboard.keyDown(fwdkey,wm)
sleep(1.5)
self.keyboard.keyUp(fwdkey,sm)
self.keyboard.keyDown(leftkey,sm)
sleep(1.75)
self.keyboard.keyUp(leftkey,wm)
self.keyboard.walk(rightkey,wm+0.25)

for i in range(width):
    for i in range(4):
        self.keyboard.walk(backkey,sm)
        self.keyboard.walk(rightkey,wm*3)
        self.keyboard.walk(backkey,sm)
        self.keyboard.walk(leftkey,wm*3)
        

    for i in range(4):
        self.keyboard.walk(fwdkey,sm)
        self.keyboard.walk(rightkey,wm*3)
        self.keyboard.walk(fwdkey,sm)
        self.keyboard.walk(leftkey,wm*3)
      

