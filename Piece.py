class Piece():

    def __init__(self, color, level, x, y, isAlive, selected, moveTurn): # initialize all properties
        self.color = color
        self.level = level
        self.pos = (x, y)
        self.isAlive = isAlive
        self.isSelected = selected
        self.moveableSquares = []
        self.moveTurn = moveTurn
        self.takingMoves = []

    def kingify(self): # increase piece level
        self.level = 2

    def calculateMoves(self, world, activePieceList):
        self.moveableSquares = []
        if self.pos[1] != 40 and self.pos[1] != 600:
            if self.isAlive and self.level == 1:
                if self.color == 'orange red': # check for orange red pieces
                    self.calcDownMoves(activePieceList)
                elif self.color == 'dodger blue': # check for dodger blue pieces
                    self.calcUpMoves(activePieceList)
            elif self.isAlive and self.level == 2:
                if self.color == 'orange red':
                    self.calcDownMoves(activePieceList)
                    self.calcUpMoves(activePieceList)
                elif self.color == 'dodger blue':
                    self.calcUpMoves(activePieceList)
                    self.calcDownMoves(activePieceList)
        elif self.pos[1] == 40:
            self.calcDownMoves(activePieceList)
            if self.color == 'dodger blue':
                self.kingify()
        elif self.pos[1] == 600:
            self.calcUpMoves(activePieceList)
            if self.color == 'orange red':
                self.kingify()



    def calculateTakes(self, world, activePieceList): # calculates captures a piece can make
        self.takingMoves = [] # empty list
        if self.pos[1] != 40 and self.pos[1] != 600:
            if self.isAlive and self.level == 1: # check if piece is alive
                if self.color == 'orange red':
                    self.calcDownTakes(activePieceList)
                elif self.color == 'dodger blue':
                    self.calcUpTakes(activePieceList)
            elif self.isAlive and self.level == 2:
                if self.color == 'orange red':
                    self.calcDownTakes(activePieceList)
                    self.calcUpTakes(activePieceList)
                elif self.color == 'dodger blue':
                    self.calcDownTakes(activePieceList)
                    self.calcUpTakes(activePieceList)
        elif self.pos[1] == 40:
            self.calcDownTakes(activePieceList)
        elif self.pos[1] == 600:
            self.calcUpTakes(activePieceList)

    def calcDownTakes(self, activePieceList):
        if activePieceList.index(self) == 0 or activePieceList.index(self) == 8 or activePieceList.index(
                self) == 16 or activePieceList.index(self) == 4 or activePieceList.index(
                self) == 12 or activePieceList.index(self) == 20:
            self.takingMoves.append(activePieceList[activePieceList.index(self) + 9])
        elif activePieceList.index(self) == 3 or activePieceList.index(self) == 11 or activePieceList.index(
                self) == 19 or activePieceList.index(self) == 7 or activePieceList.index(
                self) == 15 or activePieceList.index(self) == 23:
            self.takingMoves.append(activePieceList[activePieceList.index(self) + 7])
        elif activePieceList.index(self) <= 22:
            self.takingMoves.append(activePieceList[activePieceList.index(self) + 9])
            self.takingMoves.append(activePieceList[activePieceList.index(self) + 7])

    def calcUpTakes(self, activePieceList):
        if activePieceList.index(self) == 31 or activePieceList.index(self) == 23 or activePieceList.index(
                self) == 15 or activePieceList.index(self) == 27 or activePieceList.index(
                self) == 19 or activePieceList.index(self) == 11:
            self.takingMoves.append(activePieceList[activePieceList.index(self) - 9])
        elif activePieceList.index(self) == 28 or activePieceList.index(self) == 20 or activePieceList.index(
                self) == 12 or activePieceList.index(self) == 24 or activePieceList.index(
                self) == 16 or activePieceList.index(self) == 8:
            self.takingMoves.append(activePieceList[activePieceList.index(self) - 7])
        elif activePieceList.index(self) > 7:
            self.takingMoves.append(activePieceList[activePieceList.index(self) - 9])
            self.takingMoves.append(activePieceList[activePieceList.index(self) - 7])


    def calcDownMoves(self, activePieceList):
        if activePieceList.index(self) == 0 or activePieceList.index(self) == 7 or activePieceList.index(
                self) == 8 or activePieceList.index(self) == 15 or activePieceList.index(
                self) == 16 or activePieceList.index(self) == 23 or activePieceList.index(self) == 24:
            self.moveableSquares.append(activePieceList[activePieceList.index(self) + 4])
        elif 3 < activePieceList.index(self) < 7 or 11 < activePieceList.index(self) < 15 or 19 < activePieceList.index(
                self) < 23:
            self.moveableSquares.append(activePieceList[activePieceList.index(self) + 4])
            self.moveableSquares.append(activePieceList[activePieceList.index(self) + 5])
        elif activePieceList.index(self) < 28:
            self.moveableSquares.append(activePieceList[activePieceList.index(self) + 3])
            self.moveableSquares.append(activePieceList[activePieceList.index(self) + 4])

    def calcUpMoves(self, activePieceList):
        if activePieceList.index(self) == 31 or activePieceList.index(self) == 24 or activePieceList.index(
                self) == 23 or activePieceList.index(self) == 16 or activePieceList.index(
                self) == 15 or activePieceList.index(self) == 8 or activePieceList.index(self) == 7:
            self.moveableSquares.append(activePieceList[activePieceList.index(self) - 4])
        elif 8 < activePieceList.index(self) < 12 or 16 < activePieceList.index(
                self) < 20 or 24 < activePieceList.index(self) < 28:
            self.moveableSquares.append(activePieceList[activePieceList.index(self) - 4])
            self.moveableSquares.append(activePieceList[activePieceList.index(self) - 5])
        elif activePieceList.index(self) > 3:
            self.moveableSquares.append(activePieceList[activePieceList.index(self) - 3])
            self.moveableSquares.append(activePieceList[activePieceList.index(self) - 4])