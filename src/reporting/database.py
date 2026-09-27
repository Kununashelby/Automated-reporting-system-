import sqlite3

import pandas as pd


def get_connection(db_path="data/reporting.db"):
    """
    Create a connection to the SQLite database.
    """

    return sqlite3.connect(db_path)


def create_database(db_path="data/reporting.db"):
    """
    Create the required database tables.
    """

    connection = get_connection(db_path)

    cursor = connection.cursor()

    # ========================================================
    # SALES TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            UNIQUE(date, product, category, quantity, price, cost)
        )
        """
    )

    # ========================================================
    # REPORT HISTORY TABLE
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS report_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_time TEXT NOT NULL,
            status TEXT NOT NULL,
            records_processed INTEGER DEFAULT 0,
            total_revenue REAL DEFAULT 0,
            total_cost REAL DEFAULT 0,
            total_profit REAL DEFAULT 0,
            profit_margin REAL DEFAULT 0,
            error_message TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            report_time TEXT NOT NULL DEFAULT '18:00',
            report_format TEXT NOT NULL DEFAULT 'both',
            email_enabled TEXT NOT NULL DEFAULT 'yes',
            currency TEXT NOT NULL DEFAULT 'KSh'
        )
        """
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO settings (
            id,
            report_time,
            report_format,
            email_enabled,
            currency
        )
        VALUES (
            1,
            '18:00',
            'both',
            'yes',
            'KSh'
        )
        """
    )

    connection.commit()
    connection.close()


def import_csv_to_database(
    csv_path,
    db_path="data/reporting.db"
):
    """
    Import new sales records from CSV into SQLite.

    Duplicate records are ignored.
    """

    data = pd.read_csv(csv_path)

    connection = get_connection(db_path)

    cursor = connection.cursor()

    imported = 0
    skipped = 0

    for _, row in data.iterrows():

        try:

            cursor.execute(
                """
                INSERT INTO sales (
                    date,
                    product,
                    category,
                    quantity,
                    price,
                    cost
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row["date"],
                    row["product"],
                    row["category"],
                    int(row["quantity"]),
                    float(row["price"]),
                    float(row["cost"]),
                )
            )

            imported += 1

        except sqlite3.IntegrityError:

            skipped += 1

    connection.commit()
    connection.close()

    return imported, skipped


def load_sales_from_database(
    db_path="data/reporting.db"
):
    """
    Load all sales records from SQLite.
    """

    connection = get_connection(db_path)

    query = """
        SELECT
            date,
            product,
            category,
            quantity,
            price,
            cost
        FROM sales
    """

    data = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return data


# ============================================================
# REPORT HISTORY
# ============================================================

def save_report_history(
    status,
    records_processed=0,
    total_revenue=0,
    total_cost=0,
    total_profit=0,
    profit_margin=0,
    error_message=None,
    db_path="data/reporting.db"
):
    """
    Save the result of a report execution.
    """

    from datetime import datetime

    run_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection(db_path)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO report_history (
            run_time,
            status,
            records_processed,
            total_revenue,
            total_cost,
            total_profit,
            profit_margin,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            run_time,
            status,
            records_processed,
            total_revenue,
            total_cost,
            total_profit,
            profit_margin,
            error_message,
        )
    )

    connection.commit()
    connection.close()


def load_report_history(
    db_path="data/reporting.db"
):
    """
    Load report execution history.
    """

    connection = get_connection(db_path)

    query = """
        SELECT
            id,
            run_time,
            status,
            records_processed,
            total_revenue,
            total_cost,
            total_profit,
            profit_margin,
            error_message
        FROM report_history
        ORDER BY run_time DESC
    """

    history = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return history

def load_settings(
    db_path="data/reporting.db"
):
    connection = get_connection(db_path)

    query = """
        SELECT
            report_time,
            report_format,
            email_enabled,
            currency
        FROM settings
        WHERE id = 1
    """

    cursor = connection.cursor()

    cursor.execute(query)

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return {
            "report_time": "18:00",
            "report_format": "both",
            "email_enabled": "yes",
            "currency": "KSh",
        }

    return {
        "report_time": row[0],
        "report_format": row[1],
        "email_enabled": row[2],
        "currency": row[3],
    }


def save_settings(
    settings,
    db_path="data/reporting.db"
):
    connection = get_connection(db_path)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO settings (
            id,
            report_time,
            report_format,
            email_enabled,
            currency
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            1,
            settings["report_time"],
            settings["report_format"],
            settings["email_enabled"],
            settings["currency"],
        )
    )

    connection.commit()

    connection.close()