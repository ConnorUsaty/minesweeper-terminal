import random

SAFE = 0
MINE = 1
UNKNOWN = -1
FLAG = -2


def generate_grids():
    grid = []
    player_grid = []
    size = get_size()
    for row in range(size):
        grid.insert(row, [])
        player_grid.insert(row, [])
        for col in range(size):
            grid[row].insert(col, 0)
            player_grid[row].insert(col, -1)
    return grid, player_grid, size

def get_size():
    while True:
        size = int(input(f'How many rows and columns would you like your board to have? '))
        if 5 <= size <= 12:
            return size
        else:
            print(f'Please ensure your input is between 5 and 12!')

def difficulty_selection(size):
    difficulty = (input(f'What difficulty would you like? (Easy, Medium or Hard): ')).lower()
    while True:
        if difficulty == 'e' or difficulty == 'easy':
            print(f'You have selected easy difficulty')
            return 'Easy', (size*size//8)
        elif difficulty == 'm' or difficulty == 'medium':
            print(f'You have selected medium difficulty')
            return 'Medium', (size*size//7)
        elif difficulty == 'h' or difficulty == 'hard':
            print(f'You have selected hard difficulty')
            return 'Hard', (size*size//6)
        else:
            difficulty = input(f'Please input either \'Easy\', \'Medium\' or \'Hard\'! (\'E\', \'M\', \'H\'): ').lower()


def spawn_mines(num_mine, grid, player_grid):
    for i in range(num_mine):
        while True:
            mine_row = random.randint(0, (len(player_grid)-1))
            mine_col = random.randint(0, (len(player_grid)-1))
            if grid[mine_row][mine_col] != MINE:
                grid[mine_row][mine_col] = MINE
                break


def print_grid(player_grid):
    symbols = {UNKNOWN: '-', FLAG: 'F'}
    for row in range(len(player_grid)):
        for col in range(len(player_grid[row])):
            value = player_grid[row][col]
            if value in symbols:
                value = symbols[value]
            print(f'{value}  ', end='')
        print(f'')


def turn_decision():
    decision = input(f'Would you like to place a flag or select a square? ').lower()
    while True:
        if decision == 'f' or decision == 'flag':
            return True
        elif decision == 's' or decision == 'square':
            return False
        else:
            decision = input(f'Please select either \'Flag\' or \'Square\'! (\'F\' or \'S\'): ').lower()


def set_flag(player_grid):
    maximum = len(player_grid) - 1
    while True:
        flag_row = int(input(f'What row would you like your flag in? '))
        flag_col = int(input(f'What column would you like your flag in? '))
        flag_row -= 1
        flag_col -= 1
        if (maximum >= flag_row >= 0) and (maximum >= flag_col >= 0):
            if player_grid[flag_row][flag_col] == UNKNOWN:
                player_grid[flag_row][flag_col] = FLAG
                break
            elif player_grid[flag_row][flag_col] == FLAG:
                player_grid[flag_row][flag_col] = UNKNOWN
                break
        else:
            print(f'Please ensure your inputs are within the grid! (1-{len(player_grid)})')


def select_square(player_grid):
    maximum = len(player_grid) - 1
    while True:
        selected_row = int(input(f'Please input the row of your selected square: '))
        selected_col = int(input(f'Please input the column of your selected square: '))
        selected_row -= 1
        selected_col -= 1
        if (maximum >= selected_row >= 0) and (maximum >= selected_col >= 0):
            return selected_row, selected_col
        else:
            print(f'Please ensure your inputs are within the grid! (1-{len(player_grid)})')


def update_grid(row, col, grid, player_grid):
    maximum = len(player_grid) - 1
    surrounding_squares = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    count = 0

    for square in surrounding_squares:
        surrounding_row = row + square[0]
        surrounding_col = col + square[1]
        if (maximum >= surrounding_row >= 0) and (maximum >= surrounding_col >= 0):
            if grid[surrounding_row][surrounding_col] == MINE:
                count += 1
    player_grid[row][col] = count

    if count == 0:
        for square in surrounding_squares:
            surrounding_row = row + square[0]
            surrounding_col = col + square[1]
            if (maximum >= surrounding_row >= 0) and (maximum >= surrounding_col >= 0):
                if player_grid[surrounding_row][surrounding_col] == UNKNOWN:
                    update_grid(surrounding_row, surrounding_col, grid, player_grid)


def check_bomb(row, col, grid, player_grid):
    if grid[row][col] == MINE:
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == MINE:
                    player_grid[row][col] = 'M'
        return True
    else:
        return False


def check_win(grid, player_grid):
    for row in range(len(player_grid)):
        for col in range(len(player_grid[row])):
            if player_grid[row][col] == UNKNOWN and grid[row][col] != MINE:
                return False
            elif player_grid[row][col] == FLAG and grid[row][col] != MINE:
                return False
    return True


def main():
    grid, player_grid, size = generate_grids()
    difficulty, num_mine = difficulty_selection(size)
    spawn_mines(num_mine, grid, player_grid)
    print_grid(player_grid)
    while True:
        while True:
            if turn_decision():
                set_flag(player_grid)
                print_grid(player_grid)
            else:
                break
        row, col = select_square(player_grid)
        update_grid(row, col, grid, player_grid)
        if check_bomb(row, col, grid, player_grid):
            print_grid(player_grid)
            print(f'You hit a mine, better luck next time!')
            break
        elif check_win(grid, player_grid):
            print_grid(player_grid)
            print(f'Congratulations! You won on {difficulty} difficulty!')
            break
        else:
            print_grid(player_grid)


if __name__ == '__main__':
    main()
