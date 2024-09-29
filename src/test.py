import ast

data = {}
for i in range(1,8):
    data[i] = 0
with open("./data/user/hotbar_timings.txt", "w") as f:
    f.write(str(data))
f.close()