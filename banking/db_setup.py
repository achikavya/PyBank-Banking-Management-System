from banking.config import get_connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_no VARCHAR(15) PRIMARY KEY,
                holder_name VARCHAR(50) NOT NULL,
                pin_hash VARCHAR(64) NOT NULL,
                balance DECIMAL(15,2) NOT NULL DEFAULT 0.00,
                account_type ENUM('SAVINGS','CURRENT') NOT NULL DEFAULT 'SAVINGS',
                status ENUM('ACTIVE','INACTIVE','LOCKED') NOT NULL DEFAULT 'ACTIVE',
                failed_attempts TINYINT NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                txn_id INT AUTO_INCREMENT PRIMARY KEY,
                account_no VARCHAR(15) NOT NULL,
                txn_type ENUM('DEPOSIT','WITHDRAWAL','BALANCE_CHECK') NOT NULL,
                amount DECIMAL(15,2) DEFAULT NULL,
                balance_after DECIMAL(15,2) NOT NULL,
                description VARCHAR(255) DEFAULT NULL,
                txn_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_no)
                    REFERENCES accounts(account_no)
                    ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id INT AUTO_INCREMENT PRIMARY KEY,
                account_no VARCHAR(15) DEFAULT NULL,
                event_type VARCHAR(50) NOT NULL,
                details TEXT DEFAULT NULL,
                event_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_withdrawal_limits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_no VARCHAR(15) NOT NULL,
                limit_date DATE NOT NULL,
                total_withdrawn DECIMAL(15,2) NOT NULL DEFAULT 0.00,
                UNIQUE KEY uq_account_date (account_no, limit_date),
                FOREIGN KEY (account_no)
                    REFERENCES accounts(account_no)
                    ON DELETE CASCADE
            )
        """)

        connection.commit()
        print("All tables created successfully!")

    except Exception as e:
        connection.rollback()
        print("Error creating tables:", e)

    finally:
        cursor.close()
        connection.close()
if __name__ == "__main__":
    create_tables()