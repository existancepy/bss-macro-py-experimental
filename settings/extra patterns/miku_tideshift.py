if sizeword.lower() == "xs":
    size = 0.25/6.5
elif sizeword.lower() == "s":
    size = 0.5/6.5
elif sizeword.lower() == "l":
    size = 1/6.5
elif sizeword.lower() == "xl":
    size = 1.25/6.25
else:
    size = 0.75/6.5

self.keyboard.walk(afclrkey,7*size)
self.keyboard.walk(afcfbkey, 9*size)
self.keyboard.walk(tcfbkey, 3*size)
self.keyboard.walk(tclrkey, 3*size)
for i in range(width):
    self.keyboard.walk(tclrkey, 10*size)
    self.keyboard.walk(tcfbkey, 5*size)
    for i in range(2):
        self.keyboard.walk(afclrkey, 2*size)
        self.keyboard.walk(afcfbkey, 3*size)
        self.keyboard.walk(afclrkey, 2*size)
        self.keyboard.walk(tcfbkey, 3*size)
    self.keyboard.walk(afclrkey, 2*size)
    self.keyboard.walk(afcfbkey, 5*size)
self.keyboard.walk(afclrkey, 7*size)
self.keyboard.walk(afcfbkey, 9*size)
self.keyboard.walk(tcfbkey, 3*size)
self.keyboard.walk(tclrkey, 3*size)
for i in range(width):
    for i in range(2):
        self.keyboard.walk(tclrkey, 2*size)
        self.keyboard.walk(tcfbkey, 3*size)
        self.keyboard.walk(tclrkey, 2*size)
        self.keyboard.walk(afcfbkey, 3*size)
    self.keyboard.walk(tclrkey, 2*size)
    self.keyboard.walk(tcfbkey, 5*size)
    self.keyboard.walk(afclrkey, 12*size)
    self.keyboard.walk(afcfbkey, 5*size)
self.keyboard.walk(afclrkey, 7*size)
self.keyboard.walk(afcfbkey, 9*size)
self.keyboard.walk(tcfbkey, 8*size)
self.keyboard.walk(tclrkey, 1.5*size)
self.keyboard.press(",")
time.sleep(0.08)
for i in range(width):
    self.keyboard.walk(tclrkey, 6*size)
    self.keyboard.walk(tcfbkey, 2*size)
    self.keyboard.walk(afclrkey, 4*size)
    self.keyboard.walk(tcfbkey, 2*size)
    self.keyboard.walk(tclrkey, 4*size)
    self.keyboard.walk(tcfbkey, 2*size)
    self.keyboard.walk(afclrkey, 6*size)
    self.keyboard.walk(afcfbkey, 2*size)
    self.keyboard.walk(tclrkey, 4*size)
    self.keyboard.walk(afcfbkey, 2*size)
    self.keyboard.walk(afclrkey, 4*size)
    self.keyboard.walk(afcfbkey, 2*size)
self.keyboard.press(".")
time.sleep(0.08)
