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


for _ in range(2):
    self.keyboard.walk("s",0.5*size)
    self.keyboard.walk("a",abs(0.17*width*2))
    for _ in range(width):
        self.keyboard.walk("w",0.5*size)
        self.keyboard.walk("d",0.17)
        self.keyboard.walk("s",0.5*size)
        self.keyboard.walk("d",0.17)
    self.keyboard.walk("w",0.5*size)
    self.keyboard.walk("a",abs(0.17*width*2))
    for _ in range(width):
        self.keyboard.walk("s",0.5*size)
        self.keyboard.walk("d",0.17)
        self.keyboard.walk("w",0.5*size)
        self.keyboard.walk("d",0.17)

self.keyboard.walk("d",0.9*width)
self.keyboard.walk("w",0.4*size)
self.keyboard.walk("s",0.3*size)
self.keyboard.walk("a",0.3*width)





        
