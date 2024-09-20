exec(open("../settings/paths/cannon_to_field/pine tree.py").read())
for _ in range(2):
    self.keyboard.press(",")
self.keyboard.walk("w", 4, False)
self.keyboard.walk("a", 6, False)
self.keyboard.walk("d", 0.3, False)
self.keyboard.walk("w", 1.5, False)