import hashlib
import random

from banking.config import MAX_FAILED_ATTEMPTS
from banking.config import get_connection
from banking.exceptions import (
    AccountLockedError,
    AuthenticationError,
)
from banking.validators import (
    validate_account_type,
    validate_name,
    validate_opening_deposit,
    validate_pin,
)


def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()


def generate_account_number():
    while True:
        account_no = f"ACC{random.randint(100000000, 999999999)}"

        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute(
                "SELECT account_no FROM accounts WHERE account_no = %s",
                (account_no,)
            )

            if cursor.fetchone() is None:
                return account_no

        finally:
            cursor.close()
            connection.close()


def create_account(holder_name, pin, account_type, opening_deposit):
    holder_name = validate_name(holder_name)
    pin = validate_pin(pin)
    account_type = validate_account_type(account_type)
    opening_deposit = validate_opening_deposit(opening_deposit)

    account_no = generate_account_number()
    pin_hash = hash_pin(pin)

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO accounts
            (account_no, holder_name, pin_hash, balance, account_type)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                account_no,
                holder_name,
                pin_hash,
                opening_deposit,
                account_type,
            ),
        )

        connection.commit()

        print("\nAccount created successfully!")
        print(f"Account Number : {account_no}")
        print(f"Holder Name    : {holder_name}")
        print(f"Account Type   : {account_type}")
        print(f"Opening Balance: ₹{opening_deposit:.2f}")

        return account_no

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()


def authenticate(account_no, pin):
    pin = validate_pin(pin)

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT account_no, holder_name, pin_hash,
                   balance, account_type, status, failed_attempts
            FROM accounts
            WHERE account_no = %s
            """,
            (account_no,),
        )

        account = cursor.fetchone()

        if account is None:
            raise AuthenticationError("Account not found.")

        if account["status"] == "LOCKED":
            raise AccountLockedError("Account is locked.")

        if account["status"] != "ACTIVE":
            raise AuthenticationError("Account is not active.")

        entered_hash = hash_pin(pin)

        if entered_hash == account["pin_hash"]:
            cursor.execute(
                """
                UPDATE accounts
                SET failed_attempts = 0
                WHERE account_no = %s
                """,
                (account_no,),
            )

            connection.commit()

            print("\nLogin successful!")

            return account

        failed_attempts = account["failed_attempts"] + 1

        if failed_attempts >= MAX_FAILED_ATTEMPTS:
            cursor.execute(
                """
                UPDATE accounts
                SET failed_attempts = %s,
                    status = 'LOCKED'
                WHERE account_no = %s
                """,
                (failed_attempts, account_no),
            )

            connection.commit()

            raise AccountLockedError(
                "Account locked after 3 incorrect PIN attempts."
            )

        cursor.execute(
            """
            UPDATE accounts
            SET failed_attempts = %s
            WHERE account_no = %s
            """,
            (failed_attempts, account_no),
        )

        connection.commit()

        remaining = MAX_FAILED_ATTEMPTS - failed_attempts

        raise AuthenticationError(
            f"Incorrect PIN. {remaining} attempt(s) remaining."
        )

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print("Account module loaded successfully!")