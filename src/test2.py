#Load quest data from quest_data.txt
quest_data = {}
quest_bear = ""
quest_title = ""
quest_info = []

with open("./data/bss/quest_data.txt", "r") as f:
    qdata = [x for x in f.read().split("\n") if x]

for line in qdata:
    if line.startswith("==") and line.endswith("=="): #bear
        if quest_title:
            quest_data[quest_bear][quest_title] = quest_info  
        quest_bear = line.strip("=")
        quest_data[quest_bear] = {}
        quest_title, quest_info = "", []
    
    elif line.startswith("-"): #new quest title
        if quest_title:  
            quest_data[quest_bear][quest_title] = quest_info
        quest_title = line.lstrip("-").strip()
        quest_info = []
    
    else:  #quest objectives
        quest_info.append(line)
quest_data[quest_bear][quest_title] = quest_info  
print(quest_data)