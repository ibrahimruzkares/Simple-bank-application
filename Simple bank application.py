import random
import feedparser
from datetime import date
import time


class Account:
    def __init__(self):
        self.name = ""
        self.surname = ""
        self.bank_name = ""
        self.account_number = 0
        self.user_name = ""
        self.temp_password = 0
        self.log_user = ""
        self.log_pass = 0
        self.password = 0
        self.balance = 0

    def create_new_account(self):
        print("********Create New Account to transfer money********")
        self.bank_list()
        selection = int(input("Please enter bank reference number: "))
        match selection:
            case 1:
                self.bank_name = "Is bank"
            case 2:
                self.bank_name = "ING bank"
            case 3:
                self.bank_name = "Ak bank"

        self.name = input("Name: ")
        self.surname = input("Surname: ")
        self.account_number = "TR" + "%0.16d" % random.randint(0, 999999999999)
        self.user_name = self.name + self.surname
        self.temp_password = "%0.6d" % random.randint(0, 999999)

    @staticmethod
    def bank_list():
        bank_list = ["Is bank", "ING bank", "Ak bank"]
        codes = [1, 2, 3]
        for index, name in zip(codes, bank_list):
            print(f"{index}.{name}")

    def first_log_in(self):
        self.log_user = input("Enter your username: ")
        self.log_pass = input("Enter your Password: ")
        if self.log_user == self.user_name and self.log_pass == self.temp_password:
            print("Access granted!")
            self.password = input("Please create your new Password: ")
            self.log_pass = self.password
            print(f"You may now use your new password '{self.password}' to log in.")

    def log_in(self):
        log_in_attempts = 0
        account_blocked = False
        while not log_in_attempts >= 3:
            self.log_user = input("Enter your user name: ")
            self.log_pass = input("Enter your Password: ")
            log_in_attempts += 1
            if log_in_attempts >= 3:
                print("Your account has been blocked!")
                account_blocked = True
                if account_blocked:
                    answer = input("What was the name of your first dog?\n")
                    if answer == "lumi":
                        print("Verification succeeded!")
                        self.password = input("Create your new password: ")
                        log_in_attempts = 0
                    else:
                        print("Your account has been suspended! Contact your customer services.")
                        break
            elif self.log_user == self.user_name and self.log_pass == self.password:
                print("Welcome to Is bank mobile!")
                break
            elif self.log_user != self.user_name and self.log_pass != self.password:
                print("Wrong user ID and password!")
            elif self.log_user != self.user_name:
                print("Wrong user ID!")
            elif self.log_pass != self.password:
                print("Wrong password!")

    def show_account_details(self):
        print(f"Name: {self.name}\n"
              f"Surname: {self.surname}\n"
              f"Bank Name: {self.bank_name}\n"
              f"Account Number: {self.account_number}\n"
              f"User name: {self.user_name}\n"
              f"Temporary password: {self.temp_password}\n")


class Savings(Account):
    def __init__(self):
        super().__init__()
        self.salary = 3200
        self.days = 10
        self.saving_account_balance = 0

    def monthly_income(self):
        salary = self.salary
        days = self.days
        daily_rate = salary / 30
        partial = days % 30

        if days >= 30 and partial == 0:
            total = days // 30 * salary

        elif days >= 30 and partial != 0:
            total = (days // 30 * salary) + (partial * daily_rate)
        else:
            total = partial * daily_rate

        self.saving_account_balance += total
        self.balance += total

    def saving_account(self):
        self.monthly_income()


class Deposit(Savings):
    def __init__(self):
        super().__init__()
        self.euro_deposit = 1250
        self.usd_deposit = 1800
        self.interest_account_balance = 150000
        self.interest_rate = 0.032
        self.loan = 0

    def interest_account(self, period_month=12):
        income_tax = 0.15
        if self.interest_account_balance != 0:
            total_interest = self.interest_account_balance * self.interest_rate * period_month
            after_taxes = total_interest - (total_interest * income_tax)
            self.interest_account_balance += after_taxes
            self.balance += self.interest_account_balance

    def euro_deposit_account(self):
        euro_to_try = feedparser.parse("https://www.ecb.europa.eu/rss/fxref-try.html")["entries"]
        euro_try_exchange = float(euro_to_try[0]["title"][:5])

        total = self.euro_deposit * euro_try_exchange
        self.balance += total

    def usd_deposit_account(self):
        euro_to_try = feedparser.parse("https://www.ecb.europa.eu/rss/fxref-try.html")["entries"]
        euro_to_dollar = feedparser.parse("https://www.ecb.europa.eu/rss/fxref-usd.html")["entries"]
        euro_exchange = 1
        euro_try_exchange = float(euro_to_try[0]["title"][:5])
        euro_usd_exchange = float(euro_to_dollar[0]["title"][:5])
        usd_try_exchange = (euro_exchange / euro_usd_exchange) * euro_try_exchange

        total = self.usd_deposit * usd_try_exchange
        self.balance += total

    def overall_balance(self):
        self.saving_account()
        self.euro_deposit_account()
        self.usd_deposit_account()
        self.interest_account()

    def check_balance(self, currency):
        match currency:
            case 1:
                print(f"Dollar account balance: {round(self.usd_deposit)} USD")
            case 2:
                print(f"Euro account balance: {round(self.euro_deposit)} EURO")
            case 3:
                self.interest_account()
                print(f"Interest account balance: {round(self.interest_account_balance)} TRY")
            case 4:
                self.monthly_income()
                print(f"Saving account balance: {round(self.saving_account_balance)} TRY")
            case 5:
                self.overall_balance()
                print(f"Overall balance: {round(self.balance)} TRY")
            case 6:
                self.overall_balance()
                assets = self.balance - self.loan
                print(f"Net assets: {round(assets)} TRY")


class Transactions(Deposit):
    def __init__(self):
        super().__init__()
        self.loan = 0

    def withdraw(self, currency, amount):
        if currency == "usd":
            self.usd_deposit -= amount
        elif currency == "euro":
            self.euro_deposit -= amount
        elif currency == "try":
            self.saving_account_balance -= amount
        else:
            print("Failure!")

    def deposit_money(self, currency, amount):
        if currency == "usd":
            self.usd_deposit += amount
        elif currency == "euro":
            self.euro_deposit += amount
        elif currency == "try":
            self.saving_account_balance += amount
        elif currency == "loan":
            if self.loan >= amount:
                self.loan -= amount
            elif self.loan <= amount:
                remaining = amount - self.loan
                self.loan = 0
                print(f"{remaining} TRY will be deposit into your savings account")
                self.saving_account_balance += remaining
        else:
            print("Failure!")

    def loan_application(self):
        if self.usd_deposit >= 5000 or self.euro_deposit >= 5000 or self.saving_account_balance >= 150000:
            print(f"You are eligible to apply for a loan for {round(self.saving_account_balance * 5)} TRY. ")
            self.loan = self.saving_account_balance * 5
        elif 3000 <= self.salary <= 10000:
            print(f"You are eligible to apply for a loan for {round(self.salary * 12)} TRY. ")
            self.loan = self.salary * 12
        elif self.usd_deposit <= 1000 or self.euro_deposit <= 1000 or self.saving_account_balance <= 30000:
            print("Your credit score is not enough for loan application!")

    def transfer_money(self, sender, receiver, currency, amount):
        active = True
        while active:
            if currency == "usd":
                generate_mobile_code = "%0.4d" % random.randint(0, 9999)
                print(generate_mobile_code)
                code = input("Please enter verification code to transfer: ")
                if code == generate_mobile_code:
                    if sender.usd_deposit >= amount:
                        sender.usd_deposit -= amount
                        receiver.usd_deposit += amount
                        print(f"Transfer completed.Your final balance: {sender.usd_deposit} $")
                    answer = input("Would you like to receive your receipt(y/n): ")
                    if answer.lower() == "y":
                        self.generate_receipt(sender, receiver, amount)
                        active = False
                    else:
                        print("Thank you for chosing us!")
                        active = False
                else:
                    print("Verification code incorrect. New code will re-send in 5 seconds...")
                    time.sleep(5)


    def generate_receipt(self, sender, receiver, amount):
        print(f"""

        Your transfer details:

        Sender
        Name: {sender.name}
        Surname: {sender.surname}
        Bank Name: {sender.bank_name}
        IBAN Number: {sender.account_number}

        Receiver
        Name: {receiver.name}
        Surname: {receiver.surname}
        Bank Name: {receiver.bank_name}
        IBAN Number: {receiver.account_number}

        Amount: {amount}
        Date: {date.today()}
        Time: {time.strftime("%H:%M")}
        """)



#Sample usage
# jack = Transactions()
# jack.create_new_account()
# jack.show_account_details()
#
# george = Transactions()
# george.create_new_account()
# george.show_account_details()
# Transactions().transfer_money(jack, george, "usd", 500)
