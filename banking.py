import random
import sqlite3


class Card:
    BIN = '400000'

    def __init__(self, n=None, p=None, b=0):
        self.number = n
        self.pin = p
        self.balance = b

    def __repr__(self):
        return f"Your card number:\n{self.number}\nYour card PIN:\n{self.pin}"

    def create(self):
        account_id = str(random.randint(0, 999999999)).zfill(9)
        ck = self.checksum(self.BIN + account_id)
        self.number = self.BIN + account_id + ck
        self.pin = str(random.randint(0, 9999)).zfill(4)
        self.balance = 0
        return self

    def verify_card(self, num, pin):
        if len(num) != 16 \
                or self.checksum(num[:-1]) != num[-1]:
            return False
        if self.number == num and self.pin == pin:
            return True
        return False

    def get_balance(self):
        return self.balance

    def add_balance(self, qty):
        self.balance += qty

    @staticmethod
    def checksum(num):
        """This method returns the check digit"""
        digit_sum = 0
        for i in range(len(num)):
            digit = int(num[i])
            if i % 2 == 0:
                digit *= 2
            if digit > 9:
                digit -= 9
            digit_sum += digit
        return str((10 - digit_sum % 10) if digit_sum % 10 != 0 else 0)


DROP_CARD_TABLE = "DROP TABLE IF EXISTS card;"

CREATE_CARD_TABLE = "CREATE TABLE card " \
                    "(id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT UNIQUE, pin TEXT, balance INTEGER DEFAULT 0);"

INSERT_CARD = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);"

VERIFY_CARD_PIN = "SELECT * FROM card WHERE number = ? AND pin = ?;"

GET_CARD = "SELECT * FROM card WHERE number = ?;"

UPDATE_BALANCE = "UPDATE card SET balance = ? WHERE number = ?;"

DELETE_CARD = "DELETE FROM card WHERE number = ? AND pin = ?;"


# Connection with the DB and access functions
def connect():
    return sqlite3.connect('card.s3db')


def create_table(connection):
    with connection:
        connection.execute(DROP_CARD_TABLE)
        connection.execute(CREATE_CARD_TABLE)


def add_card(connection, number, pin, balance):
    with connection:
        connection.execute(INSERT_CARD, (number, pin, balance))


def verify_card_pin(connection, number, pin):
    with connection:
        return connection.execute(VERIFY_CARD_PIN, (number, pin)).fetchone()


def get_card(connection, number):
    with connection:
        return connection.execute(GET_CARD, (number,)).fetchone()


def update_balance(connection, number, balance):
    with connection:
        connection.execute(UPDATE_BALANCE, (balance, number))


def delete_card(connection, number, pin):
    with connection:
        connection.execute(DELETE_CARD, (number, pin))


# Main menu and relative functions
def main():
    # Create a database
    connection = connect()
    create_table(connection)
    # show main menu
    while (choice := input("\n1. Create an account\n2. Log into account\n0. Exit\n> ")) != '0':
        if choice == '1':
            create_card(connection)
        elif choice == '2':
            if card := log_in(connection):
                if login_menu(connection, card):
                    break
        else:
            print("Invalid input, please try again!")


def create_card(connection):
    card = Card().create()
    add_card(connection, card.number, card.pin, card.balance)
    print("\nYour card has been created")
    print(card)


def log_in(connection):
    user_card_number = input("\nEnter your card number:\n> ")
    user_pin = input("Enter your PIN:\n> ")
    if sel := verify_card_pin(connection, user_card_number, user_pin):
        print("\nYou have successfully logged in!")
        return Card(sel[1], sel[2], sel[3])
    print("\nWrong card number or PIN!")
    return 0


def add_income(connection, card):
    income = int(input("\nEnter income: \n"))
    card.add_balance(income)
    update_balance(connection, card.number, card.balance)
    print("Income was added!")


def do_transfer(connection, card):
    print("Transfer")
    to_card_num = input("\nEnter card number:\n")
    if to_card_num == card.number:
        print("You can't transfer money to the same account!")
        return -1
    elif card.checksum(to_card_num[:-1]) != to_card_num[-1]:
        print("Probably you made mistake in card number. Please try again!")
        return -1

    if sel := get_card(connection, to_card_num):
        to_card = Card(sel[1], sel[2], sel[3])
    else:
        print("Such a card does not exist.")
        return -1

    money = int(input("\nEnter how much money you want to transfer: \n"))
    if money > card.balance:
        print("Not enough money!")
        return -1

    card.add_balance(-money)
    update_balance(connection, card.number, card.balance)
    to_card.add_balance(money)
    update_balance(connection, to_card.number, to_card.balance)
    print("Success!")
    return None


def close_account(connection, card):
    delete_card(connection, card.number, card.pin)
    print("\nThe account has been closed!")


def login_menu(connection, card):
    menu = """\n1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n> """
    while (choice := input(menu)) != '0':
        if choice == '1':
            print(f"\nBalance: {card.get_balance()}")
        elif choice == '2':
            add_income(connection, card)
        elif choice == '3':
            do_transfer(connection, card)
        elif choice == '4':
            close_account(connection, card)
            return None
        elif choice == '5':
            print("\nYou have successfully logged out!")
            return None
        else:
            print("Invalid input, please try again!")
    return -1


if __name__ == "__main__":
    main()
