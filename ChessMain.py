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
    loadImages()

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

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