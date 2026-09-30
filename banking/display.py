from banking.config import get_connection
from banking.exceptions import TransactionError


def display_account_summary(account_no):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT account_no, holder_name, account_type,
                   balance, status, created_at
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,),
        )

        account = cursor.fetchone()

        if account is None:
            raise TransactionError("Account not found.")

        print("\n========== ACCOUNT SUMMARY ==========")
        print(f"Account Number : {account['account_no']}")
        print(f"Holder Name    : {account['holder_name']}")
        print(f"Account Type   : {account['account_type']}")
        print(f"Balance        : ₹{account['balance']:.2f}")
        print(f"Status         : {account['status']}")
        print(f"Created On     : {account['created_at']}")
        print("=====================================")

        return account

    except Exception as e:
        if isinstance(e, TransactionError):
            raise
        raise TransactionError(
            f"Unable to display account summary: {e}"
        )

    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    account_no = input("Enter test account number: ")
    display_account_summary(account_no)