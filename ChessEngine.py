"""
Responsible for storing all info about current state of chess game.
Also responsible for determining the valid moves at the current state.
"""

class GameState():

    def __init__(self):
        # board is an 8x8 2D list, each element of the list has 2 characters.
        # The first character represents color of the piece
        # The second character represents the type of the piece
        # "--" - represents an empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.whiteToMove = True
        self.moveLog = []


    '''
    Takes a move as a parameter and executes it (doesn't work for castling, pawn promotion, and en-passant )
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove # swap players
    

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            last_move = self.moveLog.pop()
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players
    

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() # for now


    '''
    All moves without considering checks    
    '''
    def getAllPossibleMoves(self):
        moves = [Move((6, 4), (4,4), self.board)]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn  = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]

                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves
    

    '''
    Get all the pawn moves for the rook location at row, col and add moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        pass


    '''
    Get all the rook moves for the rook location at row, col and add moves to the list
    '''
    def getRookMove(self, r, c, moves):
        pass
    

        

class Move():
    # map keys to values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                   "5":3 , "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                   "e": 4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board) -> None:
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        print(self.moveID)


    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]