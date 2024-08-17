class GameState:

    def __init__(self):
        # board is an 8x8 2D list, each element of the list has 2 characters.
        # The first character represents the color of the piece
        # The second character represents the type of the piece
        # "--" represents an empty space with no piece
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
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.enpassantPossible = None  # Fix: Changed from an empty tuple to None
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [
            CastleRights(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs,
            )
        ]


    '''
    Takes a move as a parameter and executes it (doesn't work for castling, pawn promotion, and en passant )
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move
        self.whiteToMove = not self.whiteToMove  # swap players

        # update king position
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # update enpassant possible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # only 2 square advances are valid
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = None  # Fix: Changed from an empty tuple to None

        # en passant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"  # capturing the pawn

        # castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # kingside castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # moves the rook
                self.board[move.endRow][move.endCol + 1] = "--" # moves the rook
            else: # queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2] # moves the rook
                self.board[move.endRow][move.endCol - 2] = "--"

        # update castling rights - whenever king or rook move
        self.updateCastleRights(move)
        self.castleRightsLog.append(
            CastleRights(
            self.currentCastlingRight.wks,
            self.currentCastlingRight.bks,
            self.currentCastlingRight.wqs,
            self.currentCastlingRight.bqs,
            )
        )

    '''
    Undo the last move made
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            last_move = self.moveLog.pop()
            self.board[last_move.startRow][last_move.startCol] = last_move.pieceMoved
            self.board[last_move.endRow][last_move.endCol] = last_move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap players

            # update king position
            if last_move.pieceMoved == 'wK':
                self.whiteKingLocation = (last_move.startRow, last_move.startCol)
            elif last_move.pieceMoved == 'bK':
                self.blackKingLocation = (last_move.startRow, last_move.startCol)

            # undo enpassant
            if last_move.isEnpassantMove:
                self.board[last_move.endRow][last_move.endCol] = "--"  # leave landing square blank
                self.board[last_move.startRow][last_move.endCol] = last_move.pieceCaptured  # leave landing square blank
                self.enpassantPossible = (last_move.endRow, last_move.startCol)
            
            if last_move.pieceMoved[1] == 'p' and abs(last_move.startRow - last_move.endRow) == 2:
                self.enpassantPossible = None  # Fix: Changed from an empty tuple to None
            
            # undo castling rights
            self.castleRightsLog.pop()  # get rid of new castlerights move
            newRights = self.castleRightsLog[-1] # set the last one as the curent
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
 

            # undo castle move
            if last_move.isCastleMove:
                if last_move.endCol - last_move.startCol == 2:
                    self.board[last_move.endRow][last_move.endCol + 1] = self.board[last_move.endRow][last_move.endCol - 1]
                    self.board[last_move.endRow][last_move.endCol - 1] = "--"
                else:
                    self.board[last_move.endRow][last_move.endCol - 2] = self.board[last_move.endRow][last_move.endCol + 1]
                    self.board[last_move.endRow][last_move.endCol + 1] = "--" 


    '''
    Update the caste rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False


    '''
    All moves considering checks
    '''
    def getValidMoves(self):
        moves = []

        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves, 'w')
        else:
            kingRow, kingCol = self.blackKingLocation
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves, 'b')
        
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow, checkCol, dRow, dCol = check
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + dRow * i, kingCol + dCol * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if (moves[i].endRow, moves[i].endCol) not in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves, 'w')
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves, 'b')
        return moves    


    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent POV
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # Switch back

        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        
        return False
    
    
    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False

        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
            
        # check outward from king for pins and checks, keep track of them
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = None  # Fix: Changed from an empty tuple to None
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin is None:  # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]

                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == 'B') or (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin is None:
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]

                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks


    '''
    All moves without considering checks    
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves
    

    '''
    Get all the pawn moves for the pawn located at row, col and add moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = None  # Fix: Changed from an empty tuple to None
        
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
        
        pawnPromotion = False

        if self.board[r + moveAmount][c] == "--":  # 1 square pawn advance
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:  # if piece gets to back row, then it is a pawn promotion
                    pawnPromotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion=pawnPromotion))

                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        
        if c - 1 >= 0:  # prevent python from wrapping from left to right
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:  # enemy piece to capture
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, isEnpassantMove=True))
                    
        if c + 1 <= len(self.board) - 1:
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:  # enemy piece to capture
                    if r + moveAmount == backRow:
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, isEnpassantMove=True))


    '''
    Get all the rook moves for the rook located at row, col and add moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = None  # Fix: Changed from an empty tuple to None
        
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':  # can't remove from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
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
    Get all the knight moves for the knight located at row, col and add moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--" or endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
               
    
    '''
    Get all the bishop moves for the bishop located at row, col and add moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = None  # Fix: Changed from an empty tuple to None
        
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:  # off board
                    break


    '''
    Get all the queen moves for the queen located at row, col and add moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    '''
    Get all the king moves for the king located at row, col and add moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    
                    inCheck, pins, checks = self.checkForPinsAndChecks()

                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)



    '''
    Generate all valid castle moves for the king at (r, c) and add them to the list of moves
    '''
    def getCastleMoves(self, r, c, moves, allyColor):
        if self.squareUnderAttack(r, c):
            return   # can't castle when in check
        
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves, allyColor)
        
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves, allyColor)
        
        
    
    def getKingSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))
    
    def getQueenSideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs) -> None:
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move:
    # map keys to values
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSq, endSq, board, isEnpassantMove=False, pawnPromotion=False, isCastleMove=False) -> None:  # Fix: corrected typo in isEnpassantMove
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion = pawnPromotion

        # En passant move
        self.isEnpassantMove = isEnpassantMove  # Fix: corrected typo

        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
        self.isCastleMove = isCastleMove


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

    '''
    Override string method
    '''
    def __str__(self):
        move_string = f"Move {self.pieceMoved} from ({self.startRow}, {self.startCol}) to ({self.endRow}, {self.endCol})"
        if self.isPawnPromotion:
            move_string += ", with pawn promotion"
        if self.isEnpassantMove:
            move_string += ", capturing en passant"
        if self.isCastleMove:
            move_string += ", with castling"

        if self.pieceCaptured != '--':
            move_string += f", capturing {self.pieceCaptured}"

        return move_string
