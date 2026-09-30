from decimal import Decimal
from banking.config import get_connection
from banking.exceptions import TransactionError
from banking.validators import validate_deposit


def deposit_money(account_no, amount):
    amount = Decimal(str(validate_deposit(amount)))

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Lock the account row while updating it
        cursor.execute(
            """
            SELECT balance, status
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (account_no,),
        )

        account = cursor.fetchone()

        if account is None:
            raise TransactionError("Account not found.")

        if account["status"] != "ACTIVE":
            raise TransactionError("Account is not active.")

        new_balance = account["balance"] + amount

        cursor.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (new_balance, account_no),
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, txn_type, amount, balance_after, description)
            VALUES (%s, 'DEPOSIT', %s, %s, %s)
            """,
            (
                account_no,
                amount,
                new_balance,
                "Cash deposit",
            ),
        )

        connection.commit()

        print("\n========== DEPOSIT RECEIPT ==========")
        print(f"Account Number : {account_no}")
        print(f"Deposited      : ₹{amount:.2f}")
        print(f"New Balance    : ₹{new_balance:.2f}")
        print("=====================================")

        return new_balance

    except Exception as e:
        connection.rollback()

        if isinstance(e, TransactionError):
            raise

        raise TransactionError(f"Deposit failed: {e}")

    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    account_no = input("Enter test account number: ")
    deposit_money(account_no, 500)