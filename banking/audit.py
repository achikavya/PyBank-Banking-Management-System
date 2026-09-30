from banking.config import get_connection


def log_event(account_no, event_type, details):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO audit_log
            (account_no, event_type, details)
            VALUES (%s, %s, %s)
            """,
            (account_no, event_type, details),
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    print("Audit module loaded successfully!")