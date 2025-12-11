def print_board(board):
    """Prints the game board"""
    print("---------")
    for row in board:
        print(f"| {' '.join(row)} |")
    print("---------")


def check_state(board):
    """Checks the current game state"""
    lines = [
        # rows
        board[0], board[1], board[2],
        # columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        # diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]

    x_wins = any(line == ["X", "X", "X"] for line in lines)
    o_wins = any(line == ["O", "O", "O"] for line in lines)
    empty_cells = any("_" in row for row in board)

    if x_wins and o_wins:
        return "Impossible"
    elif x_wins:
        return "X wins"
    elif o_wins:
        return "O wins"
    elif empty_cells:
        return "Game not finished"
    else:
        return "Draw"


def valid_coordinates(coord):
    """Checks that the coordinates are two numbers from 1 to 3"""
    if not coord.replace(" ", "").strip():
        return False
    try:
        x, y = map(int, coord.split())
        return 1 <= x <= 3 and 1 <= y <= 3
    except ValueError:
        return False


def make_move(board, player):
    """Reads coordinates from the player and makes a move"""
    while True:
        print(f"\nPlayer {player}'s turn")
        coords = input("Enter coordinates:\n> ").split()

        # Check if input is valid
        if len(coords) != 2 or not all(c.isdigit() for c in coords):
            print("You should enter numbers!")
            continue

        x, y = map(int, coords)

        # Check range
        if not (1 <= x <= 3 and 1 <= y <= 3):
            print("Coordinates should be from 1 to 3!")
            continue

        # Convert to list indices
        row = x - 1
        col = y - 1

        # Check if cell is empty
        if board[row][col] != "_":
            print("This cell is occupied! Choose another one!")
            continue

        # Make the move
        board[row][col] = player
        break


def main():
    # Create empty board
    board = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
    ]

    print_board(board)
    current_player = "X"

    while True:
        make_move(board, current_player)
        print_board(board)

        state = check_state(board)

        if state in ["X wins", "O wins", "Draw"]:
            print(state)
            break

        # Switch player
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    main()
