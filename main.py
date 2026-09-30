from getpass import getpass

from banking.account import create_account, authenticate
from banking.exceptions import BankingError
from banking.audit import log_event
from banking.deposit import deposit_money
from banking.withdraw import withdraw_money
from banking.balance import check_balance
from banking.history import get_transaction_history
from banking.display import display_account_summary


def account_menu(account):
    account_no = account["account_no"]

    while True:
        print("\n========== ACCOUNT MENU ==========")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Account Summary")
        print("6. Logout")
        print("==================================")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                amount = float(input("Enter deposit amount: "))
                deposit_money(account_no, amount)

                log_event(
                    account_no,
                    "DEPOSIT",
                    f"Deposit of ₹{amount:.2f} completed successfully."
                )

            elif choice == "2":
                amount = float(input("Enter withdrawal amount: "))
                withdraw_money(account_no, amount)

                log_event(
                    account_no,
                    "WITHDRAWAL",
                    f"Withdrawal of ₹{amount:.2f} completed successfully."
                )

            elif choice == "3":
                check_balance(account_no)

            elif choice == "4":
                get_transaction_history(account_no)

            elif choice == "5":
                display_account_summary(account_no)

            elif choice == "6":
                log_event(
                    account_no,
                    "LOGOUT",
                    "User logged out successfully."
                )

                print("\nLogged out successfully.")
                break

            else:
                print("\nInvalid choice. Please try again.")

        except BankingError as e:
            print(f"\nError: {e}")

        except ValueError:
            print("\nInvalid amount. Please enter a number.")


def main():
    while True:
        print("\n========== PYBANK ==========")
        print("1. Open New Account")
        print("2. Login Existing Account")
        print("3. Exit")
        print("============================")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                print("\n--- Open New Account ---")

                holder_name = input("Enter holder name: ")
                pin = getpass("Create 4-digit PIN: ")
                account_type = input(
                    "Enter account type (SAVINGS/CURRENT): "
                )
                opening_deposit = float(
                    input("Enter opening deposit: ")
                )

                account_no = create_account(
                    holder_name,
                    pin,
                    account_type,
                    opening_deposit
                )

                log_event(
                    account_no,
                    "ACCOUNT_CREATED",
                    f"New {account_type.upper()} account created "
                    f"for {holder_name}."
                )

            elif choice == "2":
                print("\n--- Login ---")

                account_no = input("Enter account number: ")
                pin = getpass("Enter PIN: ")

                account = authenticate(account_no, pin)

                log_event(
                    account_no,
                    "LOGIN_SUCCESS",
                    "Successful account login."
                )

                account_menu(account)

            elif choice == "3":
                print("\nThank you for using PyBank!")
                break

            else:
                print("\nInvalid choice. Please try again.")

        except BankingError as e:
            print(f"\nError: {e}")

        except ValueError:
            print("\nInvalid amount. Please enter a number.")


if __name__ == "__main__":
    main()