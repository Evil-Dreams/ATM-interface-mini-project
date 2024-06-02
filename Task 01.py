import hashlib

class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = hashlib.sha256(pin.encode()).hexdigest()  # Encrypt PIN
        self.balance = 0
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited ${amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transaction_history.append(f"Withdrew ${amount}")
        else:
            print("Insufficient funds")

    def transfer(self, amount, recipient):
        if amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
            self.transaction_history.append(f"Transferred ${amount} to {recipient.user_id}")
            recipient.transaction_history.append(f"Received ${amount} from {self.user_id}")
        else:
            print("Insufficient funds")

    def show_transaction_history(self):
        print("Transaction History:")
        for transaction in self.transaction_history:
            print(transaction)

    def change_pin(self, new_pin):
        self.pin = hashlib.sha256(new_pin.encode()).hexdigest()
        print("PIN changed successfully")

    def check_balance(self):
        print(f"Your balance is ${self.balance}")


class ATM:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        if user_id in self.users and self.users[user_id].pin == hashlib.sha256(pin.encode()).hexdigest():
            return True
        else:
            return False


def main():
    atm = ATM()

    # Adding some dummy users
    user1 = User("1234", "1234")
    user1.deposit(1000)
    atm.add_user(user1)

    user2 = User("5678", "5678")
    user2.deposit(2000)
    atm.add_user(user2)

    # ATM login
    user_id = input("Enter User ID: ")
    pin = input("Enter PIN: ")

    if atm.authenticate_user(user_id, pin):
        user = atm.users[user_id]
        while True:
            print("\nATM Menu:")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transfer")
            print("4. Transaction History")
            print("5. Change PIN")
            print("6. Check Balance")
            print("7. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                amount = float(input("Enter amount to deposit: "))
                user.deposit(amount)
            elif choice == "2":
                amount = float(input("Enter amount to withdraw: "))
                user.withdraw(amount)
            elif choice == "3":
                recipient_id = input("Enter recipient's user ID: ")
                if recipient_id in atm.users:
                    recipient = atm.users[recipient_id]
                    amount = float(input("Enter amount to transfer: "))
                    user.transfer(amount, recipient)
                else:
                    print("Recipient not found")
            elif choice == "4":
                user.show_transaction_history()
            elif choice == "5":
                new_pin = input("Enter new PIN: ")
                user.change_pin(new_pin)
            elif choice == "6":
                user.check_balance()
            elif choice == "7":
                print("Logged out successfully")
                break
            else:
                print("Invalid choice")

    else:
        print("Invalid User ID or PIN")


if __name__ == "__main__":
    main()
