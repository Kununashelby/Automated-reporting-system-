import os

from dotenv import load_dotenv

from src.reporting.database import (
    create_database,
    import_csv_to_database,
    load_sales_from_database,
)

from src.reporting.analyzer import analyze_sales

from src.reporting.charts import (
    sales_by_product,
    sales_by_category,
    revenue_cost_profit,
)

from src.reporting.pdf_report import generate_pdf_report
from src.reporting.excel_report import generate_excel_report
from src.reporting.email_report import send_report_email


# ==============================
# CONFIGURATION
# ==============================

DB_PATH = "data/reporting.db"
CSV_PATH = "data/sample_sales.csv"


# Load environment variables from .env
load_dotenv()


def main():

    # ==============================
    # 1. CREATE DATABASE
    # ==============================

    print("\n===== DATABASE SETUP =====")

    create_database(DB_PATH)

    print("Database ready.")

    # ==============================
    # 2. IMPORT NEW DATA
    # ==============================

    print("\n===== IMPORTING DATA =====")

    imported, skipped = import_csv_to_database(
        CSV_PATH,
        DB_PATH
    )

    print(f"New records imported: {imported}")
    print(f"Duplicate records skipped: {skipped}")

    # ==============================
    # 3. LOAD DATA FROM DATABASE
    # ==============================

    print("\n===== LOADING DATABASE DATA =====")

    data = load_sales_from_database(DB_PATH)

    print(f"Records loaded: {len(data)}")

    # ==============================
    # 4. ANALYZE SALES DATA
    # ==============================

    print("\n===== ANALYZING SALES DATA =====")

    results = analyze_sales(data)

    print("Sales analysis completed.")

    # ==============================
    # 5. DISPLAY SALES REPORT
    # ==============================

    print("\n===== SALES REPORT =====")

    print(
        f"Total Revenue: "
        f"KSh {results['total_revenue']:,.2f}"
    )

    print(
        f"Total Cost: "
        f"KSh {results['total_cost']:,.2f}"
    )

    print(
        f"Total Profit: "
        f"KSh {results['total_profit']:,.2f}"
    )

    print(
        f"Profit Margin: "
        f"{results['profit_margin']:.2f}%"
    )

    print(
        f"Units Sold: "
        f"{results['total_units']}"
    )

    print(
        f"Transactions: "
        f"{results['transactions']}"
    )

    # ==============================
    # 6. SALES BY PRODUCT
    # ==============================

    print("\n===== SALES BY PRODUCT =====")

    for product, revenue in results["sales_by_product"].items():

        print(
            f"{product}: "
            f"KSh {revenue:,.2f}"
        )

    # ==============================
    # 7. SALES BY CATEGORY
    # ==============================

    print("\n===== SALES BY CATEGORY =====")

    for category, revenue in results["sales_by_category"].items():

        print(
            f"{category}: "
            f"KSh {revenue:,.2f}"
        )

    # ==============================
    # 8. GENERATE CHARTS
    # ==============================

    print("\n===== GENERATING CHARTS =====")

    product_chart = sales_by_product(
        results["data"]
    )

    print(
        f"Product chart: "
        f"{product_chart}"
    )

    category_chart = sales_by_category(
        results["data"]
    )

    print(
        f"Category chart: "
        f"{category_chart}"
    )

    profit_chart = revenue_cost_profit(
        results["data"]
    )

    print(
        f"Revenue/Cost/Profit chart: "
        f"{profit_chart}"
    )

    print("\nCharts generated successfully.")

    # ==============================
    # 9. GENERATE PDF REPORT
    # ==============================

    print("\n===== GENERATING PDF REPORT =====")

    pdf_path = generate_pdf_report(results)

    print(
        f"PDF report: "
        f"{pdf_path}"
    )

    print("\nPDF report generated successfully.")

    # ==============================
    # 10. GENERATE EXCEL REPORT
    # ==============================

    print("\n===== GENERATING EXCEL REPORT =====")

    excel_path = generate_excel_report(results)

    print(
        f"Excel report: "
        f"{excel_path}"
    )

    print("\nExcel report generated successfully.")

    # ==============================
    # 11. SEND REPORT BY EMAIL
    # ==============================

    print("\n===== SENDING EMAIL =====")

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    recipient_email = os.getenv("REPORT_RECIPIENT")

    # Check email configuration
    if not sender_email:
        raise ValueError(
            "EMAIL_ADDRESS is missing from .env"
        )

    if not sender_password:
        raise ValueError(
            "EMAIL_PASSWORD is missing from .env"
        )

    if not recipient_email:
        raise ValueError(
            "REPORT_RECIPIENT is missing from .env"
        )

    # Send email
    send_report_email(
        sender_email=sender_email,
        sender_password=sender_password,
        recipient_email=recipient_email,
        subject="Automated Sales Report",
        body=f"""
Hello,

Your automated sales report has been generated successfully.

===== SALES SUMMARY =====

Total Revenue: KSh {results['total_revenue']:,.2f}
Total Cost: KSh {results['total_cost']:,.2f}
Total Profit: KSh {results['total_profit']:,.2f}
Profit Margin: {results['profit_margin']:.2f}%
Units Sold: {results['total_units']}
Transactions: {results['transactions']}

The complete PDF and Excel reports are attached to this email.

Regards,

Automated Reporting System
""",
        attachments=[
            pdf_path,
            excel_path,
        ],
    )

    print("\nEmail sent successfully.")

    # ==============================
    # 12. COMPLETE
    # ==============================

    print("\n================================")
    print("REPORTING PROCESS COMPLETED")
    print("================================")


if __name__ == "__main__":
    main()