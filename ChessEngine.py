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
        self.moveFunctions = {
            'p': self.getPawnMoves, 
            'R': self.getRookMoves,
            'N': self.getKnightMoves,
            'B': self.getBishopMoves,
            'Q': self.getQueenMoves,
            'K': self.getKingMoves
        }

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
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn  = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves
    

    '''
    Get all the pawn moves for the rook location at row, col and add moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r - 1,c), self.board))

                if r == 6 and self.board[r - 2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            
            if c-1 >= 0:  # prevent python from wrapping from left to right
                if self.board[r - 1][c - 1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            
            if c + 1 <= len(self.board) - 1:
                if self.board[r - 1][c + 1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else: # black moves
            if self.board[r + 1][c] == "--": # 1 square pawn advance
                moves.append(Move((r, c), (r + 1,c), self.board))

                if r == 1 and self.board[r + 2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            
            if c-1 >= 0:  # prevent python from wrapping from left to right
                if self.board[r + 1][c - 1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            
            if c + 1 <= len(self.board) - 1:
                if self.board[r + 1][c + 1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
    

    '''
    Get all the rook moves for the rook location at row, col and add moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        
        pass


    '''
    Get all the Knight moves for the rook location at row, col and add moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        pass

    
    '''
    Get all the Bishop moves for the rook location at row, col and add moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        pass


    '''
    Get all the Queen moves for the rook location at row, col and add moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        pass


    '''
    Get all the King moves for the rook location at row, col and add moves to the list
    '''
    def getKingMoves(self, r, c, moves):
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