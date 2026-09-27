from src.reporting.database import load_report_history


DB_PATH = "data/reporting.db"


history = load_report_history(DB_PATH)


print("\n===== REPORT HISTORY =====")

print(history)