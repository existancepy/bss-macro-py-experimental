blenderData = {
    "item": 1,
    "collectTime": 0
}
with open("data/user/blender.txt", "w") as f:
    f.write(str(blenderData))
f.close()
print(blenderData)