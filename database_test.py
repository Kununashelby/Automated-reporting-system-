from src.reporting.database import (
    create_database,
    import_csv_to_database,
    load_sales_from_database,
)


DB_PATH = "data/reporting.db"
CSV_PATH = "data/sample_sales.csv"


print("Creating database...")

create_database(DB_PATH)

print("Importing CSV data...")

imported, skipped = import_csv_to_database(
    CSV_PATH,
    DB_PATH
)

print(f"New records imported: {imported}")
print(f"Duplicate records skipped: {skipped}")

print("\nLoading data from database...")

data = load_sales_from_database(DB_PATH)

print("\n===== DATABASE DATA =====")
print(data)

print(f"\nTotal records: {len(data)}")