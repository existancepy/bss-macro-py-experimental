#update 11/24: you jump 3 times, in case you get stuck you know
#UPDATE 10/23: uh, when you have no haste you may not reach strawberry field,
#so now you go stright to the instant converter

#i believe this pattern is cool :cool: - by sev#3482
#had high haste & bear morph and still went back succesfully

#if the walk is False that means it will ignore haste, 
#which is useful for preventing failed hive reach (in this case)

#if youre near the vicious bee corner you could reduce the value by around 1-3
#===============================
self.keyboard.walk("s",3.5, False) #could reduce if near the (white) wall

self.keyboard.walk("a",3.5, False) #could reduce if near vicious
#===============================
self.keyboard.keyDown("w")
time.sleep(11)
self.keyboard.keyDown("d")
time.sleep(4)
self.keyboard.keyUp("d")
time.sleep(0.05)
self.keyboard.press("space")
time.sleep(2)
self.keyboard.press("space")
time.sleep(2.5)
self.keyboard.press("space")
time.sleep(2.5)
self.keyboard.keyUp("w")
self.keyboard.walk("s",0.35)
self.keyboard.walk("d",2, False)
self.keyboard.walk("w",0.8)
self.keyboard.multiWalk(["s","a"], 0.9)
self.keyboard.walk("d",0.25)
