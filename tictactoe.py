"""RETURN LEGEND:
-1. if the game finish with errors
 0. if the game continue
 1. if the value entered is accepted
 2. if someone wins
"""

def show_cel(matrix):
    print("--------")
    for i in range(len(matrix)):
        print("|", matrix[i][0], matrix[i][1], matrix[i][2], "|")
    print("--------")

def verify_diagram(matrix):
    """RETURNS:
    -1. if the game finish with errors
     0. if the game continue
     2. if someone wins
    """
    X_ROW = ['X', 'X', 'X']
    O_ROW = ['O', 'O', 'O']
    x_in_row = False
    o_in_row = False
    x_count = 0
    o_count = 0
    us_count = 0

    for row in matrix:
        x_count += row.count('X')
        o_count += row.count('O')
        us_count += row.count('_')
        if row == X_ROW:
            x_in_row = True
        if row == O_ROW:
            o_in_row = True

    for y in range(3):
        col = []
        for x in range(3):
            col += matrix[x][y]
        if col == X_ROW:
            x_in_row = True
        if col == O_ROW:
            o_in_row = True

    diags = [[], []]
    for i in range(3):
        diags[0] += matrix[i][i]
        diags[1] += matrix[i][2 - i]
    for diag in diags:
        if diag == X_ROW:
            x_in_row = True
        if diag == O_ROW:
            o_in_row = True

    if x_in_row and not o_in_row:
        print("X wins")
        return 2
    elif o_in_row and not x_in_row:
        print("O wins")
        return 2
    elif x_in_row and o_in_row \
            or abs(x_count - o_count) > 1:
        print("Impossible")
    elif us_count > 0:
        return 0  # print("Game not finished")
    else:
        print("Draw")
    return -1

def verify_coord(coords, matrix, turn):
    """RETURNS:
    0. to repeat entering coords
    1. if the value is accepted
    """
    PAWNS = ['X', 'O']
    for coord in coords:
        if not coord.isdigit():
            print("You should enter numbers!")
            return 0
        elif int(coord) < 1 or int(coord) > 3:
            print("Coordinates should be from 1 to 3!")
            return 0
    x = int(coords[0]) - 1
    y = 3 - int(coords[1])
    if matrix[y][x] in ['X', 'O']:
        print("This cell is occupied! Choose another one!")
        return 0
    matrix[y][x] = PAWNS[turn % 2]
    turn += 1
    return 1

turn = 0
matrix = [['_', '_', '_'] for _ in range(3)]
show_cel(matrix)

while True:
    inp_coord = input("Enter the coordinates: >").split()
    if verify_coord(inp_coord, matrix, turn) == 1:
        turn += 1
        show_cel(matrix)
    if verify_diagram(matrix) != 0:
        break
