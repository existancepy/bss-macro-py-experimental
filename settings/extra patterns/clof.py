#==================================
#brain power, activate: 
if sizeword.lower() == "xs":
    size = 0.25
elif sizeword.lower() == "s":
    size = 0.5
elif sizeword.lower() == "l":
    size = 1
elif sizeword.lower() == "xl":
    size = 1.25
else:
    size = 0.75

size = size/5.5

#changes the "nm_walk" to "self.keyboard.walk" so it can actually work for V2 
#because the logs will send an error and not use this pattern
#so best copy this for use with other natro patterns that input nm_walk
#basically "self.keyboard.walk(tcfbkey,420*size)

nm_walk = self.keyboard.walk
fwdkey = tcfbkey
backkey = afcfbkey
leftkey = tclrkey
rightkey = afclrkey
#==================================
nm_walk(leftkey,10*size)
nm_walk(backkey,10*size)
nm_walk(fwdkey,4*size)
nm_walk(rightkey,1.7*size)
for i in range(width):
	for i in range (2):
		nm_walk(rightkey,9*size)
		nm_walk(fwdkey,2*size)
		nm_walk(leftkey,9*size)
		nm_walk(fwdkey,2*size)
	for i in range (2):
		nm_walk(rightkey,9*size)
		nm_walk(backkey,2*size)
		nm_walk(leftkey,9*size)
		nm_walk(backkey,2*size)
