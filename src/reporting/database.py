import sqlite3

import pandas as pd


def get_connection(db_path="data/reporting.db"):
    """
    Create a connection to the SQLite database.
    """

    return sqlite3.connect(db_path)


def create_database(db_path="data/reporting.db"):
    """
    Create the sales table if it doesn't already exist.
    """

    connection = get_connection(db_path)

    cursor = connection.cursor()

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