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
    
wm = 0.5*size
sm = 0.25*size
df = (((wm*2)**2)+((sm*4)**2))**0.5
self.keyboard.walk("a",wm)
self.keyboard.walk("w",sm)
self.keyboard.walk("d",wm*2)
self.keyboard.walk("w",sm)
self.keyboard.walk("a",wm*2)
keyboard.press('d')
keyboard.press('s')
sleep(df)
keyboard.release('s')
keyboard.release('d')
self.keyboard.walk("a",wm*2)
self.keyboard.walk("w",sm)
self.keyboard.walk("d",wm*2)
self.keyboard.walk("w",sm*8)
self.keyboard.walk("d",0.6*width)
self.keyboard.walk("a",0.4*width)
self.keyboard.walk("s",sm*4)
self.keyboard.walk("a",wm*2)
self.keyboard.walk("s",sm)
self.keyboard.walk("d",wm*2)
self.keyboard.walk("s",sm)
self.keyboard.walk("a",wm*2)
self.keyboard.walk("s",sm)
self.keyboard.walk("d",wm*2)
self.keyboard.walk("s",sm)
self.keyboard.walk("a",wm*2)
keyboard.press('w')
keyboard.press('d')
sleep(df/2)
keyboard.release('d')
keyboard.release('w')




        
