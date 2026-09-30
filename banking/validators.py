import re

from banking.config import (
    MIN_DEPOSIT,
    MAX_DEPOSIT,
    MIN_WITHDRAWAL,
    MIN_BALANCE,
)
from banking.exceptions import ValidationError


def validate_name(name):
    name = name.strip()

    if not name:
        raise ValidationError("Holder name cannot be empty.")

    if len(name) > 50:
        raise ValidationError("Holder name cannot exceed 50 characters.")

    return name


def validate_pin(pin):
    if not re.fullmatch(r"\d{4}", pin):
        raise ValidationError("PIN must be exactly 4 digits.")

    return pin


def validate_account_type(account_type):
    account_type = account_type.strip().upper()

    if account_type not in ("SAVINGS", "CURRENT"):
        raise ValidationError("Account type must be SAVINGS or CURRENT.")

    return account_type


def validate_opening_deposit(amount):
    if amount < MIN_BALANCE:
        raise ValidationError(
            f"Opening deposit must be at least ₹{MIN_BALANCE:.2f}."
        )

    return amount


def validate_deposit(amount):
    if amount < MIN_DEPOSIT:
        raise ValidationError(
            f"Minimum deposit is ₹{MIN_DEPOSIT:.2f}."
        )

    if amount > MAX_DEPOSIT:
        raise ValidationError(
            f"Maximum deposit is ₹{MAX_DEPOSIT:.2f}."
        )

    return amount


def validate_withdrawal(amount):
    if amount < MIN_WITHDRAWAL:
        raise ValidationError(
            f"Minimum withdrawal is ₹{MIN_WITHDRAWAL:.2f}."
        )

    return amount
if __name__ == "__main__":
    print("Validator module loaded successfully!")