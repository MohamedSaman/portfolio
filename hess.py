import pygame
import time
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 800
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation
IMAGES = {}

# Initialize a dictionary of images
def loadImages():
    pieces = ['wp', 'bp', 'wn', 'bn', 'wb', 'bb', 'wR', 'bR',
              'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.image.load('images/' + piece + '.png')

# Function to convert Pygame coordinates to algebraic chess notation
def getAlgebraicNotation(spot):
    x, y = spot
    letter = chr(x + 97)
    number = 8 - y
    return letter + str(number)

# Function to convert algebraic chess notation to Pygame coordinates
def getSpot(algebraicNotation):
    x = ord(algebraicNotation[0]) - 97
    y = 8 - int(algebraicNotation[1])
    return (x, y)

# Handle player input
def handleInput(screen, board, validMoves, selectedPiece, gameOver):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            spot = pygame.mouse.get_pos()
            col = spot[0] // SQ_SIZE
            row = spot[1] // SQ_SIZE
            if not gameOver:
                if selectedPiece is None:
                    # Select a piece
                    selectedPiece = board[row][col]
                    if selectedPiece != 0 and selectedPiece.team == currentPlayer:
                        # Highlight valid moves
                        highlight(screen, board, validMoves[selectedPiece])
                else:
                    # Move the piece
                    deselect(screen)
                    new_spot = getSpot(getAlgebraicNotation((col, row)))
                    if new_spot in validMoves[selectedPiece]:
                        board[row][col] = board[selectedPiece.row][selectedPiece.col]
                        board[selectedPiece.row][selectedPiece.col] = 0
                        selectedPiece.row = row
                        selectedPiece.col = col
                        if checkMate(board, currentPlayer):
                            gameOver = True
                            print(currentPlayer, "wins by checkmate!")
                        elif checkMate(board, getOpponent(currentPlayer)):
                            gameOver = True
                            print(getOpponent(currentPlayer), "wins by checkmate!")
                        elif checkStaleMate(board):
                            gameOver = True
                            print("It's a stalemate!")
                        else:
                            currentPlayer = getOpponent(currentPlayer)
                    deselect(screen)
                    selectedPiece = None
                    highlight(screen, board, validMoves[selectedPiece])

# Highlight squares with valid moves
def highlight(screen, board, moves):
    for move in moves:
        row, col = move
        pygame.draw.rect(screen, BLUE, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw the board and pieces
def drawBoard(screen, board):
    screen.fill(WHITE)
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = GRAY if (row + col) % 2 == 0 else LIGHT_GRAY
            pygame.draw.rect(screen, color, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if board[row][col] != 0:
                screen.blit(IMAGES[board[row][col].image], (col * SQ_SIZE, row * SQ_SIZE))

# Main game loop
def main():
    global currentPlayer
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    loadImages()
    board = createBoard()
    validMoves = computeValidMoves(board)
    selectedPiece = None
    gameOver = False
    currentPlayer = 'w'

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        drawBoard(screen, board)
        handleInput(screen, board, validMoves, selectedPiece, gameOver)
        pygame.display.flip()
        clock.tick(MAX_FPS)

if __name__ == "__main__":
    main()