from decimal import Decimal
from datetime import date

from banking.config import (
    DAILY_WITHDRAWAL_LIMIT,
    MIN_BALANCE,
    get_connection,
)
from banking.exceptions import TransactionError
from banking.validators import validate_withdrawal


def withdraw_money(account_no, amount):
    amount = Decimal(str(validate_withdrawal(amount)))

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Lock the account row
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

        current_balance = account["balance"]

        # Check minimum balance
        if current_balance - amount < MIN_BALANCE:
            raise TransactionError(
                f"Minimum balance of ₹{MIN_BALANCE:.2f} must be maintained."
            )

        # Check today's withdrawal total
        today = date.today()

        cursor.execute(
            """
            SELECT total_withdrawn
            FROM daily_withdrawal_limits
            WHERE account_no = %s AND limit_date = %s
            FOR UPDATE
            """,
            (account_no, today),
        )

        daily_record = cursor.fetchone()

        if daily_record:
            withdrawn_today = daily_record["total_withdrawn"]
        else:
            withdrawn_today = 0

        if withdrawn_today + amount > DAILY_WITHDRAWAL_LIMIT:
            raise TransactionError(
                f"Daily withdrawal limit of "
                f"₹{DAILY_WITHDRAWAL_LIMIT:.2f} exceeded."
            )

        new_balance = current_balance - amount

        # Update account balance
        cursor.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (new_balance, account_no),
        )

        # Update daily withdrawal tracker
        if daily_record:
            cursor.execute(
                """
                UPDATE daily_withdrawal_limits
                SET total_withdrawn = %s
                WHERE account_no = %s AND limit_date = %s
                """,
                (withdrawn_today + amount, account_no, today),
            )
        else:
            cursor.execute(
                """
                INSERT INTO daily_withdrawal_limits
                (account_no, limit_date, total_withdrawn)
                VALUES (%s, %s, %s)
                """,
                (account_no, today, amount),
            )

        # Record transaction
        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, txn_type, amount, balance_after, description)
            VALUES (%s, 'WITHDRAWAL', %s, %s, %s)
            """,
            (
                account_no,
                amount,
                new_balance,
                "Cash withdrawal",
            ),
        )

        connection.commit()

        print("\n========= WITHDRAWAL RECEIPT =========")
        print(f"Account Number : {account_no}")
        print(f"Withdrawn      : ₹{amount:.2f}")
        print(f"New Balance    : ₹{new_balance:.2f}")
        print("=======================================")

        return new_balance

    except Exception as e:
        connection.rollback()

        if isinstance(e, TransactionError):
            raise

        raise TransactionError(f"Withdrawal failed: {e}")

    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    account_no = input("Enter test account number: ")
    withdraw_money(account_no, 100)