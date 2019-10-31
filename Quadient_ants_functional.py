def userInput(): # User input {antSymbols : numberOfAnts} for all hives
    userInputMap = {"X":4,
                    "O":3,
                    "I":5,
                    "Z":2}
    return(userInputMap)

def populateAllAnts(userInputMap): # Fill allAntsInLine with ants for all nests
    allAntsInLine = []
    for key in userInputMap:
        allAntsInLine.extend([key for i in range(userInputMap[key])])
    print(allAntsInLine)
    return(allAntsInLine)

def createMovementPriority(userInputMap): # Stores list for hive movement priority
    movementPriority = []
    for key in userInputMap: movementPriority.append(key)
    return(movementPriority)

def singleTurn(allAntsInLine, antsMovementPriority): # Process single turn movements
    positionIndex = 0
    while positionIndex < (len(allAntsInLine)-1):
        # Compare current index value to next index value and switch if not same
        if allAntsInLine[positionIndex] != allAntsInLine[positionIndex + 1] and antsMovementPriority.index(allAntsInLine[positionIndex]) < antsMovementPriority.index(allAntsInLine[positionIndex + 1]):
            allAntsInLine[positionIndex], allAntsInLine[positionIndex + 1] = allAntsInLine[positionIndex + 1], allAntsInLine[positionIndex]
            positionIndex += 1
        positionIndex +=1
    return(allAntsInLine)

def resolveAntBattle(allAntsInLine, antsMovementPriority, numberOfTurns): # Process all movement within set number of turns
    for turn in range(numberOfTurns): print(singleTurn(allAntsInLine, antsMovementPriority))
    return("Battle was finished in %d days!" %(numberOfTurns))

userInputMap = userInput()
allAntsInLine = populateAllAnts(userInputMap)
print(resolveAntBattle(allAntsInLine, createMovementPriority(userInputMap), 15))
