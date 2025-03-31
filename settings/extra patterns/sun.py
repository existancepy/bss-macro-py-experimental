#natro pattern keb-bamb by kebis.cica
#modified by your fellow sev3482

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
fwdkey = tcfbkey
backkey = afcfbkey
leftkey = tclrkey
rightkey = afclrkey
nm_walk = self.keyboard.walk
#==================================

for i in range(width):
	nm_walk(fwdkey,9*size, False)
	nm_walk(rightkey,15*size, False)
	nm_walk(leftkey,7*size)
	nm_walk(backkey,14*size)
	nm_walk(leftkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(backkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(backkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(rightkey,1*size)
	nm_walk(backkey,9*size)
	nm_walk(rightkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(rightkey,2*size)
	nm_walk(backkey,9*size)
	nm_walk(rightkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(rightkey,3*size)
	nm_walk(backkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(backkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(backkey,9*size)
	nm_walk(leftkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(rightkey,1*size)
	nm_walk(backkey,9*size)
	nm_walk(rightkey,2*size)
	nm_walk(fwdkey,9*size)
	nm_walk(rightkey,2*size)
	nm_walk(backkey,9*size)
	nm_walk(rightkey,2*size)
	nm_walk(fwdkey,9*size)
time.sleep(0.02)