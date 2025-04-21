regularMobQuantitiesInFields = {
    "rose": [("scorpion", 2)],
    "pumpkin": [("werewolf", 1)],
    "cactus": [("werewolf", 1)],
    "spider": [("spider", 1)],
    "clover": [("ladybug", 1), ("rhinobeetle", 1)],
    "strawberry": [("ladybug", 2)],
    "bamboo": [("rhinobeetle", 2)],
    "mushroom": [("ladybug", 1)],
    "blue flower": [("rhinobeetle", 1)],
    "pineapple": [("mantis", 1), ("rhinobeetle", 1)],
    "pine tree": [("mantis", 2), ("werewolf", 1)],
}
regularMobTypesInFields = {k: [x[0] for x in v] for k, v in regularMobQuantitiesInFields.items()}
print(regularMobTypesInFields)