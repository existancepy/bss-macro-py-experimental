

'''
TCFBKey:=FwdKey
 W
    AFCFBKey:=BackKey
 S
    TCLRKey:=LeftKey
 A
    AFCLRKey:=RightKey D
'''
base = 0.3 #only edit this value
    
for _ in range(width):
    self.keyboard.walk("d",base*size)
    self.keyboard.walk("s",base*size*6.8)
    self.keyboard.walk("d",base*size)
    self.keyboard.walk("w",base*size*5.6)
    self.keyboard.walk("d",base*size)
    self.keyboard.walk("s",base*size*7.36)
    self.keyboard.walk("d",base*size*1.6)
    self.keyboard.walk("w",base*size*5.6)

for _ in range(width):
    self.keyboard.walk("a",base*size)
    self.keyboard.walk("s", base*size*6)
    self.keyboard.walk("a",base*size*0.8)
    self.keyboard.walk("w",base*size*5.6)
    self.keyboard.walk("a",base*size)
    self.keyboard.walk("s",base*size*7.2)
    self.keyboard.walk("a",base*size)
    self.keyboard.walk("w",base*size*5.6)
    
    
    
    



    
    
