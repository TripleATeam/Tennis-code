def calculate(index, matches, low, high):
    size = int(high - low)
    chanceToReach = chanceToHere[index]
    if (size == 1):
        return chanceToReach
    half = low + int(size / 2)
    if size > 2:
        if index >= half:
            chanceToReach = calculate(index, matches, half, high)
        else:
            chanceToReach = calculate(index, matches, low, half)

    nonField = 0.0
    runningTotal = 0.0
    if index >= half:
        for i in range(low, half):
            chance = calculate(i, matches, low, half)
            nonField += chance
            runningTotal += chance * matches[index][i]
    else:
        for i in range(half, high):
            chance = calculate(i, matches, half, high)
            nonField += chance
            runningTotal += chance * matches[index][i]
    temp = float(chanceToReach * (runningTotal + (1.0-nonField) * matches[index][index]))
    return temp
    

size = int(input("Enter bracket size. "))
matchups = [[0.0 for i in range(size)] for j in range(size)]
names = ["" for i in range(size)]
chanceToHere = [0.0 for i in range(size)]

print("\nBracket of size " + str(size) + " selected.\n")
for i in range(size):
    name = input("Player name: ")
    chance = float(input("Chance of making it this far (0.XXX): "))
    field = float(input("Win rate against the field (0.XXX): "))
    names[i] = name
    chanceToHere[i] = chance
    matchups[i][i] = field
    print()

for i in range(size):
    for j in range(i + 1, size):
        chance = float(input("Chance of " + str(names[i]) + " beating " + str(names[j]) + " (0.XXX): "))
        matchups[i][j] = chance
        matchups[j][i] = 1 - chance
    print()

name = "y"
while name != "n":
    name = input("\nWhose chance of winning would you like to calculate? ")
    for i in range(size):
        if name == names[i]:
            percent = float(int(calculate(i, matchups, 0, size) * 10000 + 0.5))/100
            print(name + " has a " + str(percent) + "%% chance of winning.")
    name = input("Calculate another? (y/n): ")

