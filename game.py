import random

CASES = ["rock", "paper", "scissors"]


def welcome():
    score = 0
    while True:
        name = input("Enter your name: ")
        if name:
            break
    print(f"Hello, {name}")
    fl = open("rating.txt", "r")
    for line in fl:
        name_score = line.split()
        if name_score[0] == name:
            score = int(name_score[1])
    fl.close()
    return name, score


def choice_cases(default_cases):
    choice = input("")
    if choice:
        return choice.split(',')
    return default_cases


def verify_game(pl_cases, pl_choice, cp_choice, pl_score):
    offset = len(pl_cases) // 2
    pl_pos = pl_cases.index(pl_choice)
    interval = pl_cases[max(0, pl_pos-offset):pl_pos] + pl_cases[pl_pos+offset+1:]

    if pl_choice == cp_choice:
        print(f"There is a draw ({cp_choice})")
        pl_score += 50
    elif cp_choice in interval:
        print(f"Well done. The computer chose {cp_choice} and failed")
        pl_score += 100
    else:
        print(f"Sorry, but the computer chose {cp_choice}")
    return pl_score


player_name, player_score = welcome()
user_cases = choice_cases(CASES)
print("Okay, let's start")
while True:
    player_choice = input("")
    if player_choice == "!exit":
        print("Bye!")
        break
    elif player_choice == "!rating":
        print(f"Your rating: {player_score}")
    elif player_choice not in user_cases:
        print("Invalid input")
    else:
        computer_choice = random.choice(user_cases)
        player_score = verify_game(user_cases, player_choice, computer_choice, player_score)
