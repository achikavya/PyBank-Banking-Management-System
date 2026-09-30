from banking.config import get_connection
from banking.exceptions import TransactionError


def check_balance(account_no):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT balance, account_type, status
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,),
        )

        account = cursor.fetchone()

        if account is None:
            raise TransactionError("Account not found.")

        if account["status"] in ("LOCKED", "INACTIVE"):
            raise TransactionError(
                f"Balance enquiry not allowed. Account is {account['status']}."
            )

        balance = account["balance"]

        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, txn_type, amount, balance_after, description)
            VALUES (%s, 'BALANCE_CHECK', NULL, %s, %s)
            """,
            (
                account_no,
                balance,
                "Balance enquiry",
            ),
        )

        connection.commit()

        print("\n========== ACCOUNT BALANCE ==========")
        print(f"Account Number : {account_no}")
        print(f"Account Type   : {account['account_type']}")
        print(f"Status         : {account['status']}")
        print(f"Balance        : ₹{balance:.2f}")
        print("=====================================")

        return balance

    except Exception as e:
        connection.rollback()

        if isinstance(e, TransactionError):
            raise

        raise TransactionError(f"Balance enquiry failed: {e}")

    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    account_no = input("Enter test account number: ")
    check_balance(account_no)