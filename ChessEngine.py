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
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False


    '''
    Takes a move as a parameter and executes it (doesn't work for castling, pawn promotion, and en-passant )
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove # swap players

        # update king position
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
    

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            last_move = self.moveLog.pop()
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # swap players

            # update king position
            if last_move.pieceMoved == 'wK':
                self.whiteKingLocation = (last_move.startRow, last_move.startCol)
            elif last_move.pieceMoved == 'bK':
                self.blackKingLocation = (last_move.startRow, last_move.startCol)
    

    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        # 1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        # 2.) for each move, make the move
        
        for i in range(len(moves) - 1, -1, -1): # go backwards for removing elements from list
            self.makeMove(moves[i])

            self.whiteToMove = not self.whiteToMove # switch to opponent POV

            if self.inCheck():
                moves.remove(moves[i])
            
            self.whiteToMove = not self.whiteToMove # switch to opponent POV
            self.undoMove()

        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
            
        return moves # for now


    '''
    Determine if current player is inCheck
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    

    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponent POV
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # Switch back

        for move in oppMoves:
            if move.endRow == r and move.endCol == c: 
                return True
        
        return False

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
        # add pawn promotions later

    '''
    Get all the rook moves for the rook location at row, col and add moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0),  (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    '''
    Get all the Knight moves for the rook location at row, col and add moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        directions = ((-2, -1), (-2, 1), (-1, -2),  (-1, 2), (1, -2), (1, 2), (2, -1), (2,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0] 
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
               
    
    '''
    Get all the Bishop moves for the rook location at row, col and add moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1),  (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    '''
    Get all the Queen moves for the rook location at row, col and add moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    '''
    Get all the King moves for the rook location at row, col and add moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 0), (-1, 1),  (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--" or endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))    

        

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