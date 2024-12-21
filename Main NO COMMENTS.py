import pygame as p
import Piece




def setup():
    global screen, clock
    p.init()
    screen = p.display.set_mode((640, 640))
    clock = p.time.Clock()


def main():
    setup()
    drawBoard()
    pieces = makePieces()
    activePieceList = activatePieces(pieces)
    pieceSelected = False
    passGoldCirc = False
    done = False
    while not done:
        for event in p.event.get():
            if event.type == p.QUIT:
                done = True
            elif event.type == p.MOUSEBUTTONDOWN:
                click = p.mouse.get_pos()
                pieceSelected, passGoldCirc, activePieceList = selectPiece(pieces, click, activePieceList,
                                                                           pieceSelected, passGoldCirc)

        p.display.flip()
        clock.tick(20)
    p.quit()


def drawBoard():
    global world
    world = []
    board = p.draw.rect(screen, 'navajo white', (0, 0, 640, 640))
    for i in range(8):
        for j in range(8):
            if ((i + j) % 2) == 0:
                color = 'black'
                square = p.draw.rect(screen, color, (i * 80, j * 80, 80, 80))
            else:
                pass
                color = 'white'
                square = p.draw.rect(screen, color, (i * 80, j * 80, 80, 80))
            world.append(square)


def activatePieces(pieces):
    pieceList = []
    for piece in pieces:
        if 11 >= pieces.index(piece):
            pieceList.append(Piece.Piece('orange red', 1, piece.center[0], piece.center[1], True, False, False))
        elif pieces.index(piece) >= 20:
            pieceList.append(Piece.Piece('dodger blue', 1, piece.center[0], piece.center[1], True, False, True))
        else:
            pieceList.append(Piece.Piece('black', 0, piece.center[0], piece.center[1], False, False, None))
    return pieceList


def makePieces():
    pieces = []
    for j in range(len(world) // 8):
        for i in range(len(world) // 8):
            if ((i + j) % 2) == 0 and (j < 3 or j > 4):
                if j < 3:
                    color = 'orange red'
                else:
                    color = 'dodger blue'
                circle = p.draw.circle(screen, color, (80 * i + 40, 80 * j + 40), 30)
                pieces.append(circle)
            elif ((i + j) % 2) == 0:
                circle = p.draw.circle(screen, 'black', (80 * i + 40, 80 * j + 40), 30)
                pieces.append(circle)
    return pieces


def updatePieces(activePieceList, listOfPieces):
    if len(listOfPieces) != 0:
        listOfPieces = []
    for piece in activePieceList:
        if (piece.pos[1] == 600 and piece.color == 'orange red') or (
                piece.pos[1] == 40 and piece.color == 'dodger blue'):
            listOfPieces.append(Piece.Piece(piece.color, 2, piece.pos[0], piece.pos[1], piece.isAlive, piece.isSelected,
                                            not piece.moveTurn))
        elif piece.color != 'black':
            listOfPieces.append(
                Piece.Piece(piece.color, piece.level, piece.pos[0], piece.pos[1], piece.isAlive, piece.isSelected,
                            not piece.moveTurn))
        else:
            listOfPieces.append(
                Piece.Piece(piece.color, piece.level, piece.pos[0], piece.pos[1], piece.isAlive, piece.isSelected,
                            None))
        if piece.level < 2:
            p.draw.circle(screen, piece.color, (piece.pos[0], piece.pos[1]), 30)
        elif piece.color == 'dodger blue':
            p.draw.circle(screen, 'indigo', (piece.pos[0], piece.pos[1]), 30)
        elif piece.color == 'orange red':
            p.draw.circle(screen, 'pink', (piece.pos[0], piece.pos[1]), 30)
    return listOfPieces


def selectPiece(pieces, click, activePieceList, pieceSelected,
                passGoldCirc):
    selectedPiece = None
    for i in range(len(pieces)):
        for testPiece in activePieceList:
            if testPiece.isSelected:
                selectedPiece = testPiece
                break
            else:
                selectedPiece = None
        activePieceList[i].calculateTakes(world, activePieceList)
        activePieceList[i].calculateMoves(world, activePieceList)
        if (selectedPiece is not None) and (pieces[i].collidepoint(click)) and (not activePieceList[i].isAlive) and (
                activePieceList[i] in selectedPiece.takingMoves) and selectedPiece.moveTurn:
            for testPiece in activePieceList:
                if testPiece.pos == ((activePieceList[i].pos[0] + selectedPiece.pos[0]) / 2,
                                     (activePieceList[i].pos[1] + selectedPiece.pos[1]) / 2):
                    enemyPiece = testPiece
                    if enemyPiece.isAlive:
                        tempPieceList, successfulTake = takePiece(activePieceList[i], selectedPiece, enemyPiece,
                                                                  activePieceList, pieces)
                        if successfulTake:
                            passGoldCirc = pieceSelected = False
                            p.draw.circle(screen, 'black', selectedPiece.pos, 32.5, width=3)
                            return pieceSelected, passGoldCirc, tempPieceList
        elif pieces[i].collidepoint(click) and not activePieceList[i].isAlive:
            for piece in activePieceList:
                if len(piece.moveableSquares) > 0 and piece.isSelected:
                    if piece.moveTurn:
                        for square in piece.moveableSquares:
                            if not square.isAlive:
                                if pieces[activePieceList.index(square)].collidepoint(click):
                                    p.draw.circle(screen, 'black', piece.pos, 32.5, width=3)
                                    if len(activePieceList) != 0:
                                        tempPieceList = movePiece(piece, square, activePieceList)
                                        passGoldCirc = pieceSelected = False
                                        return pieceSelected, passGoldCirc, tempPieceList
        elif pieces[i].collidepoint(click) and activePieceList[i].isAlive:
            for piece in activePieceList:
                if piece.isSelected:
                    if piece == activePieceList[i]:
                        piece.isSelected = False
                        pieceSelected = False
                        p.draw.circle(screen, 'black', activePieceList[i].pos, 32.5, width=3)
                        passGoldCirc = True
                    else:
                        pieceSelected = True
            if not pieceSelected and not passGoldCirc:
                p.draw.circle(screen, 'gold', activePieceList[i].pos, 32.5, width=3)
                activePieceList[locatePiece(activePieceList[i].pos, activePieceList)].calculateMoves(world,
                                                                                                     activePieceList)
                activePieceList[i].isSelected = True
            else:
                pieceSelected = passGoldCirc = False
    return pieceSelected, passGoldCirc, activePieceList


def locatePiece(pos, activePieceList):
    for i in range(len(activePieceList)):
        if pos == activePieceList[i].pos:
            return i


def movePiece(piece, newPlace, activePieces):
    newPlace.isAlive = True
    newPlace.color = piece.color
    piece.isAlive = False
    piece.color = 'black'
    piece.isSelected = False
    piece.moveTurn = None
    newPlace.moveTurn = True
    newPlace.level = piece.level
    piece.level = 0
    activePieces = updatePieces(activePieces, activePieces)

    return activePieces


def takePiece(newPlace, oldPlace, takenPiece, activePieceList, pieces):
    if (takenPiece.color == 'orange red' and oldPlace.color == 'dodger blue') or (
            takenPiece.color == 'dodger blue' and oldPlace.color == 'orange red'):
        newPlace.isAlive = True
        newPlace.color = oldPlace.color
        newPlace.level = oldPlace.level
        newPlace.moveTurn = True
        oldPlace.isAlive = False
        oldPlace.isSelected = False
        oldPlace.color = 'black'
        oldPlace.level = 0
        oldPlace.moveTurn = None
        takenPiece.isAlive = False
        takenPiece.color = 'black'
        takenPiece.level = 0
        takenPiece.moveTurn = None
        activePieceList = updatePieces(activePieceList, activePieceList)
        return activePieceList, True
    else:
        return activePieceList, False


if __name__ == "__main__":
    main()
