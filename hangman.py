import random
import string


words = ['python', 'java', 'kotlin', 'javascript']


def print_word(word, letters):
    print("\n" + "".join([c if c in letters else "-" for c in word]))


def play():
    word_to_guess = random.choice(words)
    letter_to_guess = set(word_to_guess)
    entered_letters = set()
    guessed_letters = set()
    attempt = 8
    you_win = False
    while attempt > 0:
        print_word(word_to_guess, guessed_letters)
        letter = input("Input a letter: ")
        if len(letter) != 1:
            print("You should input a single letter")
        elif letter not in string.ascii_lowercase:
            print("It is not an ASCII lowercase letter")
        elif letter in entered_letters:
            print("You already typed this letter")
        elif letter in guessed_letters:
            print("You already typed this letter")
        elif letter in letter_to_guess:
            guessed_letters.add(letter)
            if guessed_letters == letter_to_guess:
                you_win = True
                print_word(word_to_guess, guessed_letters)
                print("You guessed the word!")
                break
        else:
            print("No such letter in the word")
            entered_letters.add(letter)
            attempt -= 1

    if you_win:
        print("You survived!")
    else:
        print("You lost!")


print("H A N G M A N")

while True:
    choice = input('\nType "play" to play the game, "exit" to quit: ')
    if choice == 'play':
        play()
    elif choice == 'exit':
        break
