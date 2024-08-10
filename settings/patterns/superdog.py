

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
    self.keyboard.walk(afclrkey,base*size)
    self.keyboard.walk(afcfbkey,base*size*6.8)
    self.keyboard.walk(afclrkey,base*size)
    self.keyboard.walk(tcfbkey,base*size*5.6)
    self.keyboard.walk(afclrkey,base*size)
    self.keyboard.walk(afcfbkey,base*size*7.36)
    self.keyboard.walk(afclrkey,base*size*1.6)
    self.keyboard.walk(tcfbkey,base*size*5.6)

for _ in range(width):
    self.keyboard.walk(tclrkey,base*size)
    self.keyboard.walk(afcfbkey, base*size*6)
    self.keyboard.walk(tclrkey,base*size*0.8)
    self.keyboard.walk(tcfbkey,base*size*5.6)
    self.keyboard.walk(tclrkey,base*size)
    self.keyboard.walk(afcfbkey,base*size*7.2)
    self.keyboard.walk(tclrkey,base*size)
    self.keyboard.walk(tcfbkey,base*size*5.6)
    
    
    
    



    
    
