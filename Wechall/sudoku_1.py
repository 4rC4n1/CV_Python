import numpy
import sys

sudokuMap = "1122223333444111222333444411112223444441112223334888515566373888855566677788885556667778DD8555667777DDDD599A6677CCCDD999AA6BBCCCDD99AAAABBBBCCD999AAABBBCCDD999AAABBBBCCC"
startingValues = {
    1 : "A", 4 : "D", 5 : "3", 8 : "7", 11 : "9",
    13 : "4", 20 : "C", 22 : "7", 23 : "B",
    26 : "6", 29 : "D", 32 : "C", 34 : "3", 36 : "8",
    40 : "B", 41 : "C", 42 : "2", 45 : "4",
    54 : "4",
    66 : "7", 68 : "5", 69 : "8", 71 : "3",
    79 : "5", 80 : "B", 84 : "2",
    92 : "3", 98 : "5", 100 : "2", 103 : "8",
    108 : "A", 112 : "4", 113 : "5",
    118 : "C", 126 : "D", 128 : "3",
    130 : "B", 135 : "9",    
    144 : "4", 148 : "2", 149 : "D", 151 : "8",    
    160 : "5", 161 : "6", 162 : "A",    
    } 

listOfValues = ["1","2","3","4","5","6","7","8","9","A","B","C","D"]   
    
class Cell:
    def __init__(self, cellID, clusterID, row, col, values):
        self.id = cellID
        self.cluster = clusterID
        self.row = row
        self.col = col
        self.values = values
    
    def removeValue(self, value):
        self.values = self.values.replace(value, " ")
 
class Sudoku:
    def __init__(self, numberOfRows, numberOfCols):
        counter = 0
        mapIndex = 0
        self.loopBreaker = True
        self.testTry = False
        self.deadEndCounter = 0
        self.sudokuList = []
        self.numberOfCols = numberOfCols
        for nrow in range(0, numberOfRows):
            for icol in range(0, numberOfCols):
                self.sudokuList.append(Cell(counter, sudokuMap[mapIndex],nrow,icol,"[123456789ABCD]"))
                counter += 1
                mapIndex += 1
        
        for key in startingValues:
            self.finalCellValue(key, startingValues[key])
            
    def finalCellValue(self,cellID,desiredValue):
        self.sudokuList[cellID].values = "|      " + desiredValue + "      |"
        self.eliminatorCheck()       
 
    def eliminatorCheck(self):
        for elem in self.sudokuList:
            if "|" in elem.values:
                self.eliminate(elem.values[7], elem.id, elem.col, elem.row, elem.cluster)
        
                
    def eliminate(self, elimValue, protectedID, col, row, cluster):
        for item in self.sudokuList:
            if "|" not in item.values and item.id != protectedID and (item.col == col or item.row == row or str(item.cluster) == str(cluster)):
                item.removeValue(elimValue)


    def drawSudoku(self):
        self.checkClustersForUnique()
        i = 0
        if self.testTry == False:
            while i < len(self.sudokuList)-1:
                for col in range(0,self.numberOfCols):
                    print(self.sudokuList[i].values, end =" ")
                    i += 1
                print("")
        elif self.testTry == True:
            print(self.buildSolution())
        self.buildSolution()

    def checkClustersForUnique(self):
        breaker = False
        for clusterValue in listOfValues:
            cluster = []
            for item in self.sudokuList:
                if str(item.cluster) == clusterValue and item.values[0] != "|":
                    cluster.append(item)
            self.checkValuesForUnique(cluster)        
            cluster = []

    def checkValuesForUnique(self, cluster):
        breaker = False
        uniqueValues = []
        for itemValue in listOfValues:
            for item in cluster:
                if itemValue in item.values:
                    uniqueValues.append(item.id)

            if len(uniqueValues) == 1:
                print("removed" + str(uniqueValues[0]))
                self.deadEndCounter = 0
                self.finalCellValue(uniqueValues[0],itemValue)
                uniqueValues=[]
                breaker = True
                break
#            if len(uniqueValues) == 3:
#                print(itemValue, uniqueValues, self.sudokuList[int(uniqueValues[0])].values, self.sudokuList[uniqueValues[1]].values, self.sudokuList[uniqueValues[2]].values)
            uniqueValues = []
            if breaker == True:
                break
        self.deadEndCounter += 1 
        if self.deadEndCounter >= 10 and self.testTry == False:
            self.deadEnd()
        elif self.deadEndCounter >= 10 and self.testTry == True:
            self.deadEndCounter = 0
            self.loopBreaker = False
    
    def buildSolution(self):
        solution = ""
        for item in self.sudokuList:
            if item.values[0] == "|":
                solution = solution + str(item.values[7])
        return(solution.lower())

    def deadEnd(self):
        self.lastSolvedCount = self.countSolvedFields(self.sudokuList)
        print("Je vyřešeno: ", self.lastSolvedCount)
        user = input("Pokračovat?")
        if user == "a":
            sys.exit()
        else:
            self.deadEndCounter = 0
            self.bruteForceSolver()

        
    def bruteForceSolver(self):
        self.backupData = self.sudokuList
        self.count = self.lastSolvedCount
        for item in self.sudokuList:
            if "[" == item.values[0]:
                testCases = item.values.replace(" ","").replace("[", "").replace("]","")
                for char in testCases:
                    print (testCases, char)                   
                    self.testTry = True
                    print(item.id)
                    self.finalCellValue(item.id,char)
                    self.solveSudoku()
                    if self.count < self.lastSolvedCount:
                        self.count = self.lastSolvedCount
                        goodID = item.id
                        goodChar = char
                        print(item.id, char)
                    self.sudokuList = self.backupData
        self.sudokuList[goodID].values = "[      " + goodChar + "      ]"
        self.testTry = False            

    def solveSudoku(self):
        while self.loopBreaker == True:
            self.drawSudoku()
        self.loopBreaker = False    

    def countSolvedFields(self, data):
        numberOfSolved = 0
        for item in data:
            if "|" in item.values:
                numberOfSolved += 1
        return(numberOfSolved)
        
            
test = Sudoku(13,13)
test.solveSudoku()
