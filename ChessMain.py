"""
Main driver file. Responsible for user input and display
"""
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8  # 8x8 board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bB', 'bN', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

'''
This is our main driver. We get user input and update states.
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made

    loadImages()

    sqSelected = () #no square is selected initially, keep track of last click by user
    playClicks = [] #keep track of player clicks
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            # mouse event handlers
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square twice
                    sqSelected = ()
                    playClicks = []
                else:
                    sqSelected = (row, col)
                    playClicks.append(sqSelected) # append for both 1st and 2nd click

                if len(playClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playClicks[0], playClicks[1], gs.board)

                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playClicks = []
                    else:
                        playClicks = [sqSelected]
            # key handlers
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
            
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

    p.quit()

'''
Responsible for all the graphics within a current game state
'''
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on board

    #add in piece highlighting or move suggestion (later)

    drawPieces(screen, gs.board) 


'''
Draw the squares on the board. The top left is always white
'''
def drawBoard(screen):
    colors = [p.Color('white'), p.Color('gray')]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
           color = colors[((r + c) % 2)] 
           p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    

'''
Draw the pieces on the board using the current Gamestate.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]

            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
 


if __name__ == "__main__":
    main()
