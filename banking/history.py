from banking.config import get_connection
from banking.exceptions import TransactionError


def get_transaction_history(account_no, limit=10):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT txn_id, txn_type, amount, balance_after,
                   description, txn_date
            FROM transactions
            WHERE account_no = %s
            ORDER BY txn_date DESC, txn_id DESC
            LIMIT %s
            """,
            (account_no, limit),
        )

        transactions = cursor.fetchall()

        if not transactions:
            print("\nNo transactions found.")
            return []

        print("\n========== TRANSACTION HISTORY ==========")
        print(f"Account Number : {account_no}")
        print("-----------------------------------------")

        for txn in transactions:
            amount = (
                f"₹{txn['amount']:.2f}"
                if txn["amount"] is not None
                else "-"
            )

            print(f"Transaction ID : {txn['txn_id']}")
            print(f"Type           : {txn['txn_type']}")
            print(f"Amount         : {amount}")
            print(f"Balance After  : ₹{txn['balance_after']:.2f}")
            print(f"Description    : {txn['description']}")
            print(f"Date           : {txn['txn_date']}")
            print("-----------------------------------------")

        return transactions

    except Exception as e:
        raise TransactionError(
            f"Unable to fetch transaction history: {e}"
        )

    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    account_no = input("Enter test account number: ")
    get_transaction_history(account_no)