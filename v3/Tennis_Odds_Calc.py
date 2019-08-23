import requests
import json

H2H_WEIGHT = 0.0
INPUT_WEIGHT = 0.0
RANKING_WEIGHT = 1.0

def calculate(index, matches, low, high, chanceToHere):
    size = int(high - low)
    chanceToReach = chanceToHere[index]
    if (size == 1):
        return chanceToReach
    half = low + int(size / 2)
    if size > 2:
        if index >= half:
            chanceToReach = calculate(index, matches, half, high, chanceToHere)
        else:
            chanceToReach = calculate(index, matches, low, half, chanceToHere)

    nonField = 0.0
    runningTotal = 0.0
    if index >= half:
        for i in range(low, half):
            chance = calculate(i, matches, low, half, chanceToHere)
            nonField += chance
            runningTotal += chance * matches[index][i]
    else:
        for i in range(half, high):
            chance = calculate(i, matches, half, high, chanceToHere)
            nonField += chance
            runningTotal += chance * matches[index][i]
    temp = float(chanceToReach * (runningTotal + (1.0-nonField) * matches[index][index]))
    return temp
    
def main():
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
                percent = float(int(calculate(i, matchups, 0, size, chanceToHere) * 10000 + 0.5))/100
                print(name + " has a " + str(percent) + "%% chance of winning.")
        name = input("Calculate another? (y/n): ")

def read():
    f = open("playerInfo.txt", "r")
    #"size = 128"
    size = int(f.readline()[6:])
    matchups = [[0.0 for i in range(size)] for j in range(size)]
    names = ["" for i in range(size)]
    chanceToHere = [0.0 for i in range(size)]
    i = 0
    for line in f:
        strings = line.split()
        name = ""
        for i in range(len(strings)-2):
            name += strings[i] + " "
        name = name.rstrip()
        names[i] = name
        chanceToHere[i] = float(strings[-2])
        matchups[i][i] = float(strings[-1])
        i = i + 1
    
    f = open("matchups.txt", "r")
    i = 0
    for line in f:
        strings = line.split()
        for j in range(i+1,len(strings)):
            matchups[i][j] = float(strings[j])
            matchups[j][i] = 1-float(strings[j])
        i = i + 1

    name = "y"
    while name != "n":
        name = input("\nWhose chance of winning would you like to calculate? ")
        for i in range(size):
            if name == names[i]:
                percent = float(int(calculate(i, matchups, 0, size, chanceToHere) * 10000 + 0.5))/100
                print(name + " has a " + str(percent) + "%% chance of winning.")
        name = input("Calculate another? (y/n): ")
        
def readWebsiteWins(name1, name2):
    name1url = name1.replace(" ", "%20")
    name2url = name2.replace(" ", "%20")
    URL = "http://www.matchstat.com/tennis/h2h-odds-bets/" + name1url + "/" + name2url
    r = requests.get(url = URL)
    if "No previous matches" in r.text:
        return 1, 1
    sub1 = r.text.find(name1, 10000)
    sub2 = r.text.find(name2, 10000)
    sub = 0
    if sub2 < sub1:
        sub = sub2 #name2 comes before name1
    else:
        sub = sub1 #name1 comes before name2
    winsStart = r.text.find("Wins:</td><td>", sub) + 14
    winsEnd = r.text.find("</td>", winsStart)
    #print(str(winsStart) + " " + str(winsEnd))
    #print(r.text[winsStart:winsStart+2000])
    wins1 = int(r.text[winsStart:winsEnd])
    winsStart = r.text.find("Wins:</td><td>", winsEnd) + 14
    winsEnd = r.text.find("</td>", winsStart)
    wins2 = int(r.text[winsStart: winsEnd])
    #print(r.text[10000:15000])
    #print(str(wins1) + " " + str(wins2))
    if (sub1 < sub2):
        return wins1, wins2
    return wins2, wins1

def smartRead():
    f = open("playerInfo.txt", "r")
    #"size = 128"
    size = int(f.readline()[6:])
    matchups = [[0.0 for i in range(size)] for j in range(size)]
    names = ["" for i in range(size)]
    chanceToHere = [0.0 for i in range(size)]
    ranking = [0 for i in range(size)]
    i = 0
    for line in f:
        strings = line.split()
        name = ""
        for j in range(len(strings)-3):
            name += strings[j] + " "
        name = name.rstrip()
        names[i] = name
        chanceToHere[i] = float(strings[-3])
        matchups[i][i] = float(strings[-2])
        ranking[i] = int(strings[-1])
        i = i + 1
    
    if (INPUT_WEIGHT != 0.0):
        f = open("matchups.txt", "r")
        i = 0
        for line in f:
            strings = line.split()
            for j in range(i+1,len(strings)):
                matchups[i][j] = float(strings[j])
                matchups[j][i] = 1-float(strings[j])
            i = i + 1
    
    query = input("Update H2H list? (y/n): ")
    i = 0
    if (query == "y"):
        f = open("H2H.txt", "w+")
        for i in range(len(names)):
            for j in range(i+1,len(names)):
                print("Calculating " + names[i] + " versus " + names[j])
                wins1, wins2 = readWebsiteWins(names[i], names[j])
                f.write(str(wins1) + " " + str(wins2) + "\n")
                sum = wins1 + wins2
                ranking1 = ranking[j]/(ranking[j]+ranking[i]) * RANKING_WEIGHT
                ranking2 = ranking[i]/(ranking[j]+ranking[i]) * RANKING_WEIGHT
                matchups[i][j] = INPUT_WEIGHT * matchups[i][j] + H2H_WEIGHT * float(wins1)/sum + ranking1
                matchups[j][i] = INPUT_WEIGHT * matchups[j][i] + H2H_WEIGHT * float(wins2)/sum + ranking2
            i = i + 1
        f.close()
    else:
        f = open("H2H.txt", "r+")
        i = 0
        j = 1
        for line in f:
            strings = line.split()
            wins1 = int(strings[0])
            wins2 = int(strings[1])
            if (j >= len(names)):
                i += 1
                j = i + 1
            sum = wins1 + wins2
            ranking1 = ranking[j]/(ranking[j]+ranking[i]) * RANKING_WEIGHT
            ranking2 = ranking[i]/(ranking[j]+ranking[i]) * RANKING_WEIGHT
            matchups[i][j] = INPUT_WEIGHT * matchups[i][j] + H2H_WEIGHT * float(wins1)/sum + ranking1
            matchups[j][i] = INPUT_WEIGHT * matchups[j][i] + H2H_WEIGHT * float(wins2)/sum + ranking2
            j += 1

    name = "y"
    while name != "n":
        name = input("\nWhose chance of winning would you like to calculate? ")
        for i in range(size):
            if name == names[i]:
                percent = float(int(calculate(i, matchups, 0, size, chanceToHere) * 10000 + 0.5))/100
                print(name + " has a " + str(percent) + "%% chance of winning.")
        name = input("Calculate another? (y/n): ")

#def chance(wins, total, weight):
    

response = "y"
while (response != "q"):
    response = input("Would you like to read data from a file? (y/n/s): ")
    if (response == "y"):
        read()
    elif (response == "n") :
        main()
    elif (response == "s"):
        #readWebsiteWins("Kei Nishikori", "Daniil Medvedev")
        smartRead()
    response = input("Hit 'q' to exit or any key to continue. ")

