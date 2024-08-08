
self.keyboard.walk("a",(0.25*size))
self.keyboard.walk("w",(0.25*size))
for i in range(width):
    if i != 0:
        self.keyboard.walk("a",(0.2*i)/2)
        self.keyboard.walk("w",(0.2*i)/2)
    self.keyboard.walk("d",0.5*size+0.2*i)
    self.keyboard.walk("s",0.5*size+0.2*i)
    self.keyboard.walk("a",0.5*size+0.2*i)
    self.keyboard.walk("w",0.5*size+0.2*i)

for i in range(width,0,-1):
    print(i)
    if i != width:
        self.keyboard.walk("s",(0.2*i)/2)
        self.keyboard.walk("d",(0.25*i)/2)
    self.keyboard.walk("d",0.5*size+0.2*i)
    self.keyboard.walk("s",0.5*size+0.2*i)
    self.keyboard.walk("a",0.5*size+0.2*i)
    self.keyboard.walk("w",0.5*size+0.2*i)

    
self.keyboard.walk("s",0.25*size)
self.keyboard.walk("d",0.25*size)

    
 

    
    
