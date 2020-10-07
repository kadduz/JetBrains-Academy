import sys
import math

CHOICES = ['n', 'a', 'p', 'd']
TYPES = ['annuity', 'diff']


def calculate_months(principal, montly_amount, interest):
    interest_rate = interest / 100 / 12
    total_months = math.ceil(math.log(montly_amount / (montly_amount - interest_rate * principal), 1 + interest_rate))
    years = total_months // 12
    months = total_months - 12 * years
    overpayment = math.floor(montly_amount * total_months - principal)

    str_years = ""
    if years > 0:
        s = ""
        if years > 1:
            s = "s"
        str_years = f"{years} year{s} "
    andstr = ""
    if years > 0 and months > 0:
        andstr = "and "
    str_months = ""
    if months > 0:
        s = ""
        if months > 1:
            s = "s"
        str_months = f"{months} month{s} "
    print(f"It will take {str_years}{andstr}{str_months}to repay this loan!")
    if overpayment > 0:
        print(f"Overpayment = {overpayment}")


def calculate_payment(principal, periods, interest):
    interest_rate = interest / 100 / 12
    int_pow = math.pow(1 + interest_rate, periods)
    payments = math.ceil(principal * (interest_rate * int_pow) / (int_pow - 1))
    overpayment = math.floor(payments * periods - principal)
    out = f"Your monthly payment = {payments}!"
    print(out)
    if overpayment > 0:
        print(f"Overpayment = {overpayment}")


def calculate_loan(annuity, periods, interest):
    interest_rate = interest / 100 / 12
    int_pow = math.pow(1 + interest_rate, periods)
    principal = math.floor(annuity / ((interest_rate * int_pow) / (int_pow - 1)))
    overpayment = math.floor(annuity * periods - principal)
    print(f"Your loan principal = {principal}!")
    if overpayment > 0:
        print(f"Overpayment = {overpayment}")


def calculate_differentiated(principal, periods, interest):
    overpayment = - principal
    interest_rate = interest / 100 / 12
    for month in range(1, periods + 1):
        month_payment_f = (principal / periods) +\
                        interest_rate * (principal - principal * (month - 1) / periods)
        month_payment = math.ceil(month_payment_f)
        print(f"Month {month}: payment is {month_payment}")
        overpayment += month_payment
    if overpayment > 0:
        print(f"\nOverpayment = {overpayment}")


def send_error(error="Incorrect parameters."):
    print(error)
    exit()
    

args = sys.argv

loan_principal = 0
montly_payment = 0
loan_interest = 0
months_num = 0

interactive_mode = False
if len(args) == 1:
    # Execution by interactive menu
    interactive_mode = True
    while True:
        print("""What do you want to calculate?
        type "n" for number of monthly payments,
        type "a" for annuity monthly payment amount,
        type "p" for loan principal:
        type "d" for Differentiate payment""")
        choice = input()
        if choice in CHOICES:
            break
else:
    # Execution by command line
    choice = ""
    i_type = ""
    verify = [False, False, False, False, False]  # [type, principal, periods, interest, payments]
    if args[1].startswith("--type="):
        i_type = args[1].lstrip("--type=")
        if i_type in TYPES:
            verify[0] = True
        else:
            send_error()
    else:
        send_error()

    for arg in args[2:]:
        if arg.startswith("--principal="):
            loan_principal = int(arg.lstrip("--principal="))
            verify[1] = True
        if arg.startswith("--periods="):
            months_num = int(arg.lstrip("--periods="))
            verify[2] = True
        if arg.startswith("--interest="):
            loan_interest = float(arg.lstrip("--interest="))
            verify[3] = True
        if arg.startswith("--payment="):
            montly_payment = int(arg.lstrip("--payment="))
            verify[4] = True

    if i_type == 'diff':
        verify[4] = True  # payments
        if all(verify):
            choice = "d"
        else:
            send_error()
    else:
        if verify.count(False) != 1:
            send_error()
        pos = verify.index(False)
        if pos == 1:
            choice = "p"
        elif pos == 2:
            choice = "n"
        elif pos == 4:
            choice = "a"
        else:
            send_error()

if choice == 'n':
    if interactive_mode:
        loan_principal = int(input("Enter the loan principal:\n"))
        montly_payment = int(input("Enter the monthly payment:\n"))
        loan_interest = float(input("Enter the loan interest:\n"))
    calculate_months(loan_principal, montly_payment, loan_interest)
elif choice == 'a':
    if interactive_mode:
        loan_principal = int(input("Enter the loan principal:\n"))
        months_num = int(input("Enter the number of periods:\n"))
        loan_interest = float(input("Enter the loan interest:\n"))
    calculate_payment(loan_principal, months_num, loan_interest)
elif choice == 'p':
    if interactive_mode:
        montly_payment = float(input("Enter the annuity payment:\n"))
        months_num = int(input("Enter the number of periods:\n"))
        loan_interest = float(input("Enter the loan interest:\n"))
    calculate_loan(montly_payment, months_num, loan_interest)
elif choice == 'd':
    if interactive_mode:
        loan_principal = int(input("Enter the loan principal:\n"))
        months_num = int(input("Enter the number of periods:\n"))
        loan_interest = float(input("Enter the loan interest:\n"))
    calculate_differentiated(loan_principal, months_num, loan_interest)
