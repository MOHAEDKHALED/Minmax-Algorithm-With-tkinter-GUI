import tkinter as tk
from tkinter import messagebox

# Board size and colors
BOARD_SIZE = 3
BACKGROUND_COLOR = '#FFFFFF'
LINE_COLOR = '#000000'
PLAYER_COLOR = '#FF0000'
COMPUTER_COLOR = '#0000FF'

# Initialize the game board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Initialize the GUI
root = tk.Tk()
root.title("Tic Tac Toe")

# Create canvas for drawing the game board
canvas = tk.Canvas(root, width=300, height=300, bg=BACKGROUND_COLOR)
canvas.pack()


def draw_board():
    # Draw horizontal lines
    for i in range(1, BOARD_SIZE):
        canvas.create_line(0, i * 100, 300, i * 100, fill=LINE_COLOR, width=4)

    # Draw vertical lines
    for i in range(1, BOARD_SIZE):
        canvas.create_line(i * 100, 0, i * 100, 300, fill=LINE_COLOR, width=4)


def draw_symbols():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x = j * 100 + 50
            y = i * 100 + 50
            symbol = board[i][j]
            if symbol == 'X':
                canvas.create_line(x - 25, y - 25, x + 25, y + 25, fill=PLAYER_COLOR, width=8)
                canvas.create_line(x + 25, y - 25, x - 25, y + 25, fill=PLAYER_COLOR, width=8)
            elif symbol == 'O':
                canvas.create_oval(x - 25, y - 25, x + 25, y + 25, outline=COMPUTER_COLOR, width=8)


def is_board_full():
    for row in board:
        if ' ' in row:
            return False
    return True


def is_winner(symbol):
    # Check rows
    for row in board:
        if all(cell == symbol for cell in row):
            return True

    # Check columns
    for j in range(BOARD_SIZE):
        if all(board[i][j] == symbol for i in range(BOARD_SIZE)):
            return True

    # Check diagonal
    if all(board[i][i] == symbol for i in range(BOARD_SIZE)):
        return True

    # Check reverse diagonal
    if all(board[i][BOARD_SIZE - 1 - i] == symbol for i in range(BOARD_SIZE)):
        return True

    return False



def evaluate():
    if is_winner('X'):
        return -1  # Player wins
    elif is_winner('O'):
        return 1  # Computer wins
    else:
        return 0  # Draw


def minimax(depth, is_maximizing_player):
    score = evaluate()

    if score == 1 or score == -1:
        return score

    if is_board_full():
        return 0
# o role 
    if is_maximizing_player:
        best_score = float('-inf')

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(depth + 1, False)
                    board[i][j] = ' '

                    best_score = max(score, best_score)

        return best_score
    else:
        best_score = float('inf')

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(depth + 1, True)
                    board[i][j] = ' '

                    best_score = min(score, best_score)

        return best_score


def make_computer_move():
    best_score = float('-inf')
    best_move = None

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(0, False)
                board[i][j] = ' '

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move:
        i, j = best_move
        board[i][j] = 'O'
        draw_symbols()

        if is_winner('O'):
            messagebox.showinfo("Game Over", "Computer Wins!")
            root.quit()
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a Draw!")
            root.quit()


def make_player_move(event):
    if is_board_full() or is_winner('X') or is_winner('O'):
        return

    x = event.x // 100
    y = event.y // 100

    if board[y][x] == ' ':
        board[y][x] = 'X'
        draw_symbols()

        if is_winner('X'):
            messagebox.showinfo("Game Over", "You Win!")
            root.quit()
        elif is_board_full():
            messagebox.showinfo("Game Over", "It's a Draw!")
            root.quit()

        make_computer_move()


# Bind the player's move to mouse clicks
canvas.bind("<Button-1>", make_player_move)


# Draw the initial game board
draw_board()

# Start the game loop
root.mainloop()
