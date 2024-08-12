
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
    
wm = 0.2*size
sm = 0.65*size
self.keyboard.walk(tclrkey,width*wm*2)
self.keyboard.walk(afcfbkey,sm)
for _ in range(width):
    self.keyboard.walk(afclrkey,wm)
    self.keyboard.walk(tcfbkey,sm)
    self.keyboard.walk(afclrkey,wm)
    self.keyboard.walk(afcfbkey,sm)
    
self.keyboard.walk(tclrkey,width*wm*2)
self.keyboard.walk(tcfbkey,sm)
for _ in range(width):
    self.keyboard.walk(afclrkey,wm)
    self.keyboard.walk(afcfbkey,sm)
    self.keyboard.walk(afclrkey,wm)
    self.keyboard.walk(tcfbkey,sm)


        
