
ct = loadsettings.load()["canon_time"]

self.keyboard.slowPress(",")
self.keyboard.slowPress(",")
self.keyboard.slowPress("e")
time.sleep(0.8)
self.keyboard.keyDown("w")
self.keyboard.slowPress("space")
self.keyboard.slowPress("space")
sleep(2.6*ct)
self.keyboard.slowPress(".")
self.keyboard.slowPress(".")
sleep(3.55*ct)
self.keyboard.keyUp("w")
self.keyboard.slowPress("space")
sleep(0.8)

    
