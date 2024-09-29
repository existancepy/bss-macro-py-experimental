with open("../settings/paths/cannon_to_field/blue flower.py", "r") as f:
    blueFlowerPath = f.read()
f.close()

compareBlueFlowerPath = '\nself.keyboard.press(",")\nself.keyboard.press(",")\nself.keyboard.slowPress("e")\nsleep(0.08)\nself.keyboard.keyDown("w")\nself.keyboard.slowPress("space")\nself.keyboard.slowPress("space")\nsleep(3)\nself.keyboard.keyUp("w")\nself.keyboard.slowPress("space")\nsleep(0.8)'
print(compareBlueFlowerPath == blueFlowerPath)