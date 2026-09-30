# PyBank - Banking Management System

## Description

PyBank is a Python-based Banking Management System developed using Python and MySQL. It provides secure account management, authentication, deposits, withdrawals, balance checking, transaction history, and audit logging.

## Features

- Create Savings and Current accounts
- Secure 4-digit PIN authentication
- SHA-256 PIN hashing
- Account locking after 3 incorrect PIN attempts
- Deposit and withdrawal operations
- Minimum balance validation
- Daily withdrawal limit
- Balance enquiry
- Transaction history
- Account summary
- Audit logging
- MySQL database integration
- Row-level locking for transactions

## Technology Stack

- Python 3
- MySQL
- mysql-connector-python
- SQL
- VS Code
- Git and GitHub

## Project Structure

```text
banking_system/
│
├── main.py
├── requirements.txt
├── README.md
│
└── banking/
    ├── __init__.py
    ├── config.py
    ├── db_setup.py
    ├── exceptions.py
    ├── validators.py
    ├── account.py
    ├── deposit.py
    ├── withdraw.py
    ├── balance.py
    ├── history.py
    ├── display.py
    └── audit.py
```

## Business Rules

| Rule | Value |
|---|---:|
| Minimum opening balance | ₹1,000 |
| Minimum deposit | ₹500 |
| Maximum deposit | ₹100,000 |
| Minimum withdrawal | ₹100 |
| Minimum required balance | ₹1,000 |
| Daily withdrawal limit | ₹50,000 |
| PIN length | 4 digits |
| Maximum failed PIN attempts | 3 |

## Setup and Installation

### 1. Clone or download the project

Open the project folder in VS Code.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure MySQL

Create a MySQL database named:

```sql
CREATE DATABASE banking_db;
```

Update your MySQL password in:

```text
banking/config.py
```

### 4. Create the database tables

Run:

```bash
python -m banking.db_setup
```

### 5. Run the application

Run:

```bash
python main.py
```

## Usage

After starting the application, the main menu provides:

1. Open New Account
2. Login Existing Account
3. Exit

After successful login, users can:

1. Deposit
2. Withdraw
3. Check Balance
4. Transaction History
5. Account Summary
6. Logout

## Security

- PINs are stored using SHA-256 hashing.
- PIN input is hidden using `getpass`.
- Accounts are locked after 3 incorrect PIN attempts.
- Database transactions use row-level locking for safe concurrent operations.

## Database

The application uses the following tables:

- `accounts`
- `transactions`
- `audit_log`
- `daily_withdrawal_limits`

## Author

Developed as a Python and MySQL Banking Management System project.