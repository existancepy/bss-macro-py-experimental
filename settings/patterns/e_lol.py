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


self.keyboard.walk(afcfbkey,0.5*size)
self.keyboard.walk(tclrkey,abs(0.17*width*2))
for _ in range(width):
    self.keyboard.walk(tcfbkey,0.5*size)
    self.keyboard.walk(afclrkey,0.17)
    self.keyboard.walk(afcfbkey,0.5*size)
    self.keyboard.walk(afclrkey,0.17)
self.keyboard.walk(tcfbkey,0.5*size)
self.keyboard.walk(tclrkey,abs(0.17*width*2))
for _ in range(width):
    self.keyboard.walk(afcfbkey,0.5*size)
    self.keyboard.walk(afclrkey,0.17)
    self.keyboard.walk(tcfbkey,0.5*size)
    self.keyboard.walk(afclrkey,0.17)




        
