import random


def main():
    possible_choices = ('user', 'easy', 'medium', "hard")
    while (inp_str := input("Input command: ").strip()) != 'exit':
        choices = inp_str.split()
        if len(choices) != 3 or choices[0] != 'start' \
                or choices[1] not in possible_choices \
                or choices[2] not in possible_choices:
            print("Bad parameters!")
        else:
            play(choices[1], choices[2])


def play(x_player, o_player):
    schema = [[' ', ' ', ' '] for _ in range(3)]  # empty schema
    player_pawn = 'X'  # first player
    show_schema(schema)
    while True:
        player = x_player if player_pawn == 'X' else o_player
        coords = take_coords(schema, player, player_pawn)
        schema[coords[1]][coords[0]] = player_pawn
        show_schema(schema)
        if verify_diagram(schema, player_pawn) != 0:
            break
        player_pawn = 'O' if player_pawn == 'X' else 'X'  # next player
    return None


def show_schema(schema):
    print("--------")
    for row in schema:
        print(f"| {' '.join(row)} |")
    print("--------")


def take_coords(schema, player, player_pawn):
    if player == 'user':
        while (coord := player_coord(schema)) == -1:
            pass
    else:
        coord = computer_coord(schema, player, player_pawn)
    return coord


def player_coord(schema):
    coords = input("Enter the coordinates: ").split()
    for coord in coords:
        if not coord.isdigit():
            print("You should enter numbers!")
            return -1
        elif len(coords) != 2:
            print("You should enter two numbers!")
            return -1
        elif int(coord) < 1 or int(coord) > 3:
            print("Coordinates should be from 1 to 3!")
            return -1
    x = int(coords[0]) - 1
    y = 3 - int(coords[1])
    if schema[y][x] in ('X', 'O'):
        print("This cell is occupied! Choose another one!")
        return -1
    return x, y


def computer_coord(schema, level, player_pawn):
    print(f'Making move level "{level}"')
    if level == 'medium':
        return level_medium(schema, player_pawn)
    elif level == 'hard':
        coord, _ = level_hard(schema, player_pawn, player_pawn)
        return coord
    # level = 'easy'
    empty_cells = find_empty_cells(schema)
    return random.choice(empty_cells)


def find_empty_cells(schema):
    empty_cells = []
    for y, row in enumerate(schema):
        empty_cells.extend([(x, y) for x in range(len(row)) if schema[y][x] not in ('X', 'O')])
    return empty_cells


def level_medium(schema, player_pawn):
    empty_cells = find_empty_cells(schema)
    # verify if there are two same symbols in a row to win
    for coords in empty_cells:
        new_schema = [row[:] for row in schema]  # create a copy of current schema
        new_schema[coords[1]][coords[0]] = player_pawn
        if verify_diagram(new_schema, player_pawn, check_schema=True) == 1:
            return coords
    # check if there are two same symbols in a row that make the opponent win
    for coords in empty_cells:
        new_schema = [row[:] for row in schema]  # create a copy of current schema
        opponent_pawn = 'O' if player_pawn == 'X' else 'X'
        new_schema[coords[1]][coords[0]] = opponent_pawn
        if verify_diagram(new_schema, opponent_pawn, check_schema=True) == 1:
            return coords
    return random.choice(empty_cells)


def level_hard(schema, player_pawn, original_pawn):
    scores = {}
    empty_cells = find_empty_cells(schema)

    for coords in empty_cells:
        new_schema = [row[:] for row in schema]  # create a copy of current schema
        new_schema[coords[1]][coords[0]] = player_pawn
        response = verify_diagram(new_schema, player_pawn, check_schema=True)
        if response == -1:  # nor winner nor draw
            opponent_pawn = 'O' if player_pawn == 'X' else 'X'
            _, scores[coords] = level_hard(new_schema, opponent_pawn, original_pawn)
        else:
            if player_pawn == original_pawn:
                scores[coords] = response
            else:
                scores[coords] = -1 * response
    if player_pawn == original_pawn:
        coord = max(scores, key=scores.get)
    else:
        coord = min(scores, key=scores.get)
    score = scores[coord]
    return coord, score


def verify_diagram(schema, player_pawn, check_schema=False):
    pawn_wins = False
    x_count = 0
    o_count = 0

    diags = [[], []]
    for y, row in enumerate(schema):
        x_count += row.count('X')
        o_count += row.count('O')

        col = []
        for x in range(len(row)):  # build column
            col += schema[x][y]

        diags[0] += schema[y][y]  # build main diagonal
        diags[1] += schema[y][2 - y]  # build second diagonal
        if row.count(player_pawn) == 3 or col.count(player_pawn) == 3:
            pawn_wins = True
    if diags[0].count(player_pawn) == 3 or diags[1].count(player_pawn) == 3:
        pawn_wins = True

    if check_schema:
        if pawn_wins:
            return 1
        elif x_count + o_count == 9:
            return 0  # Draw
    else:
        if pawn_wins:
            print(f"{player_pawn} wins")
        elif abs(x_count - o_count) > 1:
            print("Impossible")
        elif x_count + o_count == 9:
            print("Draw")
        else:
            return 0
    return -1


if __name__ == '__main__':
    main()
