import random

# Constants for the game grid
ROWS = 6
COLUMNS = 7

def clear_grid(grid):
    for row in range(ROWS):
        for col in range(COLUMNS):
            grid[row][col] = ' '

def display_grid(grid):
    for row in grid:
        print(" ".join(row).replace(' ', '_').replace('*', '(*)').replace('o', 'o'))
    print("1 2 3 4 5 6 7")  # Display column numbers for reference

def is_valid_move(grid, column):
    return grid[0][column] == ' '

def drop_disc(grid, column, color):
    for row in range(ROWS - 1, -1, -1):
        if grid[row][column] == ' ':
            grid[row][column] = color
            break

def count_aligned_discs(grid, row, col, color):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    max_alignment = 0

    for dr, dc in directions:
        alignment = 0
        r, c = row, col

        while 0 <= r < ROWS and 0 <= c < COLUMNS and grid[r][c] == color:
            alignment += 1
            r, c = r + dr, c + dc

        r, c = row, col

        while 0 <= r >= 0 and 0 <= c >= 0 and grid[r][c] == color:
            alignment += 1
            r, c = r - dr, c - dc

        alignment -= 1

        if alignment > max_alignment:
            max_alignment = alignment

    return max_alignment

def recommend_column_improved(grid, color):
    valid_columns = [col for col in range(COLUMNS) if is_valid_move(grid, col)]
    best_column = None
    best_alignment = -1

    for col in valid_columns:
        for row in range(ROWS - 1, -1, -1):
            if grid[row][col] == ' ':
                alignment = count_aligned_discs(grid, row, col, color)
                if alignment >= 3:
                    return col

                if alignment > best_alignment:
                    best_alignment = alignment
                    best_column = col

    return best_column if best_column is not None else random.choice(valid_columns)

def main():
    grid = [[' ' for _ in range(COLUMNS)] for _ in range(ROWS)]

    player_color = 'Y'
    computer_color = 'R'
    player_turn = True

    while True:
        display_grid(grid)

        if player_turn:
            column_to_play = int(input("Your turn. Enter a column (1-7): ")) - 1
            if is_valid_move(grid, column_to_play):
                drop_disc(grid, column_to_play, player_color)
            else:
                print("Invalid move. Try again.")
                continue
        else:
            column_to_play = recommend_column_improved(grid, computer_color)
            drop_disc(grid, column_to_play, computer_color)

        if count_aligned_discs(grid, ROWS - 1, column_to_play, player_color) >= 4:
            display_grid(grid)
            print("Congratulations! You win!")
            break

        if count_aligned_discs(grid, ROWS - 1, column_to_play, computer_color) >= 4:
            display_grid(grid)
            print("The computer wins. Better luck next time!")
            break

        player_turn = not player_turn

if __name__ == "__main__":
    main()

