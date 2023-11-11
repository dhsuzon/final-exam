import random

class Bank:
    def __init__(self):
        self.users = []
        self.loans_enabled = True
        self.bank_balance = 0
        self.loan_amount = 0

    def generate_account_number(self):
        return random.randint(1000, 9999)
    
    def find_user(self, name):
        return next((u for u in self.users if u.name.lower() == name.lower()), None)

    def create_account(self, name, email, address, account_type):
        existing_user = self.find_user(name)
        if existing_user:
            print(f"Account for user '{name}' already exists.")
            return self.replica_system(existing_user)

        account_number = self.generate_account_number()
        user = User(account_number, name, email, address, account_type)
        self.users.append(user)
        print(f"Account created successfully for user '{name}' with account number {account_number}.")
        return user
    
    def delete_account(self, name):
        user = self.find_user(name)
        if user:
            self.users.remove(user)
            print(f"User account for '{name}' deleted successfully.")
        else:
            print(f"User account for '{name}' not found.")

    def see_all_accounts_list(self):
        if not self.users:
            print("No user accounts found.")
        else:
            print("All user accounts:")
            for user in self.users:
                print(f'Account_number: {user.account_number}, Name: {user.name}')

    def check_total_available_balance(self):
        total_balance = sum(user.balance for user in self.users)
        return total_balance
    
    def check_total_loan_amount(self):
        return self.loan_amount
    
    def loan_feature(self):
        self.loans_enabled = not self.loans_enabled
        if self.loans_enabled:
            print("Loan feature is now enabled.")
        else:
            print("Loan feature is now disabled.")

    def replica_system(self, existing_user):
        print("Do you want to create a new account or return to the main menu?")
        while True:
            choice = input("Enter '1' for a new account, '2' to return to the main menu: ")
            if choice == '1':
                return self.create_account(input("Enter Your Name: "),
                                           input("Enter Your Email: "),
                                           input("Enter Your Address: "),
                                           input("Enter Your Account Type (Savings/Current): ").capitalize())
            elif choice == '2':
                return existing_user
            else:
                print("Invalid choice. Please enter '1' or '2'.")

class User:
    def __init__(self, account_number, name, email, address, account_type):
        self.account_number = account_number
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = 0
        self.transaction_history = []
        self.take_loan = 0

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f'deposited: {amount}')
        print("Deposit successful.")

    def withdraw(self, amount, bank):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
        else:
            self.balance -= amount
            self.transaction_history.append(f'withdrew: {amount}')
            print("Withdrawal successful.")

    def check_available_balance(self):
        return self.balance
    
    def check_transaction_history(self):
        return self.transaction_history
    
    def take_a_loan(self, amount, bank):
        if bank.loans_enabled and self.take_loan < 2:
            if self.balance >= amount:
                self.take_loan += 1
                self.balance += amount
                bank.loan_amount += amount
                self.transaction_history.append(f'loan_taken: {amount}')
                print("Loan taken successfully.")
            else:
                print("Insufficient funds to take a loan.")
        elif not bank.loans_enabled:
            print("Bank is bankrupt")
        else:
            print("You've already taken the maximum number of loans")

    def transfer_the_amount(self, amount, recipient, bank):
        if amount > self.balance:
            print("Insufficient funds")
        elif not recipient:
            print("Account does not exist")
        else:
            self.balance -= amount
            recipient.deposit(amount)
            self.transaction_history.append(f'transferred: {amount}')
            print("Amount transferred successfully.")

# main program
bank = Bank()

while True:
    print("Welcome to the Banking Management System")
    print("1. User Operations")
    print("2. Admin Operations")
    print('3. Exit')

    option = input("Enter Your Option: ")

    if option == '1':
        print('User operations start')
        user_name = input("Enter Your Name: ")
        user_email = input("Enter Your Email: ")
        user_address = input("Enter Your Address: ")
        user_account_type = input("Enter Your Account Type (Savings/Current): ").capitalize()

        user = bank.create_account(user_name, user_email, user_address, user_account_type)
        while True:
            print('User Menu:')
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Available Balance")
            print("4. Check Transaction History")
            print("5. Take a Loan")
            print("6. Transfer the Amount")
            print("7. Back to Main Menu")

            user_option = input("Enter your user option (1 to 7): ")

            if user_option == '1':
                amount = float(input("Enter the deposit amount: "))
                user.deposit(amount)

            elif user_option == '2':
                amount = float(input("Enter the withdraw amount: "))
                user.withdraw(amount, bank)

            elif user_option == '3':
                print("Available balance", user.check_available_balance())
            elif user_option == '4':
                print("Transaction history:")
                for transaction in user.check_transaction_history():
                    print(transaction)
            elif user_option == '5':
                amount = float(input("Enter the loan amount: "))
                user.take_a_loan(amount, bank)

            elif user_option == '6':
                recipient_name = input("Enter recipient name: ")
                recipient = bank.find_user(recipient_name)
                if recipient:
                    amount = float(input("Enter the transfer amount: "))
                    user.transfer_the_amount(amount, recipient, bank)
            elif user_option == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    elif option == '2':
        print('Admin operations start')

        admin_name = input("Enter your name: ")
        admin_email = input("Enter your email: ")
        admin_address = input("Enter your address: ")
        admin_type = input("Enter your account type (Admin): ").capitalize()

        admin = bank.create_account(admin_name, admin_email, admin_address, admin_type)

        while True:

            print("Admin menu:")
            print("1. Create User Account")
            print("2. Delete User Account")
            print("3. See All Accounts List")
            print("4. Check Total Available Balance")
            print("5. Check Total Loan Amount")
            print("6. Loan Feature")
            print("7. Back to Main Menu")

            admin_option = input("Enter your option (1 to 7): ")

            if admin_option == '1':
                user_name = input("Enter user's name: ")
                user_email = input("Enter user's email: ")
                user_address = input("Enter user's address: ")
                user_type = input("Enter user's account type (Savings/Current): ")

                bank.create_account(user_name, user_email, user_address, user_type)
                print("User account created successfully")

            elif admin_option == '2':
                user_name = input("Enter user's name to delete the account: ")
                bank.delete_account(user_name)

            elif admin_option == '3':
                print("Show all accounts list")
                bank.see_all_accounts_list()
            elif admin_option == '4':
                print("Check total available balance")
                print("Total available balance:", bank.check_total_available_balance())

            elif admin_option == '5':
                print("Total loan amount")
                print("Total loan amount:", bank.check_total_loan_amount())
            
            elif admin_option == '6':
                print("Loan feature")
                bank.loan_feature()

            elif admin_option == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    elif option == '3':
        print("Exiting the Banking Management System. Thank you!")
        break

    else:
        print("Invalid choice. Please try again.")
