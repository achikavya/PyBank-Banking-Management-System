class BankingError(Exception):
    """Base exception for banking application."""
    pass


class ValidationError(BankingError):
    """Raised when input validation fails."""
    pass


class AuthenticationError(BankingError):
    """Raised when authentication fails."""
    pass


class AccountLockedError(BankingError):
    """Raised when an account is locked."""
    pass


class InsufficientBalanceError(BankingError):
    """Raised when the account does not have enough balance."""
    pass


class TransactionError(BankingError):
    """Raised when a banking transaction fails."""
    pass