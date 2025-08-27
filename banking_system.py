import mysql.connector

# BankAccount class handles all operations related to the bank account
class BankAccount:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()
        
    # Create a new account with name and PIN 
    def create_account(self, name, pin):
        sql = "INSERT INTO accounts (name, pin, balance) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (name, pin, 0))
        self.db.commit()
        print(f"✅ Account created for {name}. Account Number: {self.cursor.lastrowid}")
        
    # Deposit amount into a specific account
    def deposit(self, acc_no, amount):
        sql = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"
        self.cursor.execute(sql, (amount, acc_no))
        self.db.commit()
        if self.cursor.rowcount:
            print(f"✅ Deposited ₹{amount} to Account No {acc_no}")
        else:
            print("❌ Account not found.")
    # Withdraw amount after PIN verification
    def withdraw(self, acc_no,pin,amount):
        self.cursor.execute("SELECT balance FROM accounts WHERE account_number = %s AND pin = %s", (acc_no,pin))
        result = self.cursor.fetchone()
        if result:
            current_balance = result[0]
            if current_balance >= amount:
                sql = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s"
                self.cursor.execute(sql, (amount, acc_no))
                self.db.commit()
                print(f"✅ Withdrew ₹{amount} from Account No {acc_no}")
            else:
                print("❌ Insufficient funds.")
        else:
            print("❌ Account not found.")
            
    # Check balance after verifying PIN
    def check_balance(self, acc_no, pin):
        sql = "SELECT name, balance FROM accounts WHERE account_number = %s AND pin = %s"
        self.cursor.execute(sql, (acc_no, pin))
        result = self.cursor.fetchone()
        if result:
            name, balance = result
            print(f"👤 Account Holder: {name}")
            print(f"💰 Balance: ₹{balance}")
        else:
            print("❌ Invalid account number or PIN.")
            
# Main function to run the banking system
def main():
    # Connect to MySQL database
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="", 
            database="banking_system"
        )
    except mysql.connector.Error as err:
        print("Error connecting to database:", err)
        return

    bank = BankAccount(db)
    
    # Menu-driven console interface
    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter your name: ")
            pin = int(input("Set a 4-digit PIN: "))
            bank.create_account(name, pin)
        elif choice == '2':
            acc_no = int(input("Enter Account Number: "))
            amount = float(input("Enter amount to deposit: "))
            bank.deposit(acc_no, amount)
        elif choice == '3':
            acc_no = int(input("Enter Account Number: "))
            pin = int(input("Enter your PIN: "))
            amount = float(input("Enter amount to withdraw: "))
            bank.withdraw(acc_no,pin, amount)
        elif choice == '4':
            acc_no = int(input("Enter Account Number: "))
            pin = int(input("Enter your PIN: "))
            bank.check_balance(acc_no, pin)
        elif choice == '5':
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice. Try again.")

    db.close()

if __name__ == "__main__":
    main()
