if sizeword.lower() == "xs":
    size = 0.5
elif sizeword.lower() == "s":
    size = 1
elif sizeword.lower() == "l":
    size = 2
elif sizeword.lower() == "xl":
    size = 2.5
else:
    size = 1.5


for _ in range(2):
    move.hold("s",0.5*size)
    move.hold("a",abs(0.17*width*2))
    for _ in range(width):
        move.hold("w",0.5*size)
        move.hold("d",0.17)
        move.hold("s",0.5*size)
        move.hold("d",0.17)
    move.hold("w",0.5*size)
    move.hold("a",abs(0.17*width*2))
    for _ in range(width):
        move.hold("s",0.5*size)
        move.hold("d",0.17)
        move.hold("w",0.5*size)
        move.hold("d",0.17)

move.hold("d",0.9*width)
move.hold("w",0.4*size)
move.hold("s",0.3*size)
move.hold("a",0.3*width)





        
