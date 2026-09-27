import os

from dotenv import load_dotenv

from src.reporting.database import (
    create_database,
    import_csv_to_database,
    load_sales_from_database,
    load_settings,
    save_report_history,
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


# ============================================================
# CONFIGURATION
# ============================================================

DB_PATH = "data/reporting.db"
CSV_PATH = "data/sample_sales.csv"


# Load environment variables
load_dotenv()


# ============================================================
# MAIN REPORTING SYSTEM
# ============================================================

def main():

    try:

        # ====================================================
        # 1. CREATE DATABASE
        # ====================================================

        print("\n===== DATABASE SETUP =====")

        create_database(DB_PATH)

        print("Database ready.")

        # ====================================================
        # 2. LOAD SYSTEM SETTINGS
        # ====================================================

        print("\n===== LOADING SETTINGS =====")

        settings = load_settings(DB_PATH)

        report_format = settings.get(
            "report_format",
            "both"
        )

        email_enabled = settings.get(
            "email_enabled",
            "yes"
        )

        currency = settings.get(
            "currency",
            "KSh"
        )

        print(
            f"Report format: {report_format}"
        )

        print(
            f"Email enabled: {email_enabled}"
        )

        print(
            f"Currency: {currency}"
        )

        # ====================================================
        # 3. IMPORT NEW DATA
        # ====================================================

        print("\n===== IMPORTING DATA =====")

        imported, skipped = import_csv_to_database(
            CSV_PATH,
            DB_PATH
        )

        print(f"New records imported: {imported}")
        print(f"Duplicate records skipped: {skipped}")

        # ====================================================
        # 4. LOAD DATA FROM DATABASE
        # ====================================================

        print("\n===== LOADING DATABASE DATA =====")

        data = load_sales_from_database(DB_PATH)

        print(f"Records loaded: {len(data)}")

        # ====================================================
        # 5. ANALYZE SALES DATA
        # ====================================================

        print("\n===== ANALYZING SALES DATA =====")

        results = analyze_sales(data)

        print("Sales analysis completed.")

        # ====================================================
        # 6. DISPLAY SALES REPORT
        # ====================================================

        print("\n===== SALES REPORT =====")

        print(
            f"Total Revenue: "
            f"{currency} {results['total_revenue']:,.2f}"
        )

        print(
            f"Total Cost: "
            f"{currency} {results['total_cost']:,.2f}"
        )

        print(
            f"Total Profit: "
            f"{currency} {results['total_profit']:,.2f}"
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

        # ====================================================
        # 7. SALES BY PRODUCT
        # ====================================================

        print("\n===== SALES BY PRODUCT =====")

        for product, revenue in results[
            "sales_by_product"
        ].items():

            print(
                f"{product}: "
                f"{currency} {revenue:,.2f}"
            )

        # ====================================================
        # 8. SALES BY CATEGORY
        # ====================================================

        print("\n===== SALES BY CATEGORY =====")

        for category, revenue in results[
            "sales_by_category"
        ].items():

            print(
                f"{category}: "
                f"{currency} {revenue:,.2f}"
            )

        # ====================================================
        # 9. GENERATE CHARTS
        # ====================================================

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

        # ====================================================
        # 10. GENERATE PDF REPORT
        # ====================================================

        pdf_path = None

        if report_format in ("both", "pdf"):

            print("\n===== GENERATING PDF REPORT =====")

            pdf_path = generate_pdf_report(results)

            print(
                f"PDF report: "
                f"{pdf_path}"
            )

            print(
                "\nPDF report generated successfully."
            )

        else:

            print(
                "\n===== PDF REPORT SKIPPED ====="
            )

        # ====================================================
        # 11. GENERATE EXCEL REPORT
        # ====================================================

        excel_path = None

        if report_format in ("both", "excel"):

            print("\n===== GENERATING EXCEL REPORT =====")

            excel_path = generate_excel_report(results)

            print(
                f"Excel report: "
                f"{excel_path}"
            )

            print(
                "\nExcel report generated successfully."
            )

        else:

            print(
                "\n===== EXCEL REPORT SKIPPED ====="
            )

        # ====================================================
        # 12. SEND REPORT BY EMAIL
        # ====================================================

        if email_enabled == "yes":

            print("\n===== SENDING EMAIL =====")

            sender_email = os.getenv(
                "EMAIL_ADDRESS"
            )

            sender_password = os.getenv(
                "EMAIL_PASSWORD"
            )

            recipient_email = os.getenv(
                "REPORT_RECIPIENT"
            )

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

            # Build available attachments
            attachments = []

            if pdf_path:
                attachments.append(pdf_path)

            if excel_path:
                attachments.append(excel_path)

            # Build report description
            generated_reports = []

            if pdf_path:
                generated_reports.append("PDF")

            if excel_path:
                generated_reports.append("Excel")

            report_description = " and ".join(
                generated_reports
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

Total Revenue: {currency} {results['total_revenue']:,.2f}
Total Cost: {currency} {results['total_cost']:,.2f}
Total Profit: {currency} {results['total_profit']:,.2f}
Profit Margin: {results['profit_margin']:.2f}%
Units Sold: {results['total_units']}
Transactions: {results['transactions']}

Generated reports:
{report_description}

Regards,

Automated Reporting System
""",
                attachments=attachments,
            )

            print("\nEmail sent successfully.")

        else:

            print(
                "\n===== EMAIL DISABLED ====="
            )

            print(
                "Email sending skipped because "
                "email is disabled in settings."
            )

        # ====================================================
        # 13. SAVE SUCCESS HISTORY
        # ====================================================

        save_report_history(
            status="SUCCESS",
            records_processed=len(data),
            total_revenue=results["total_revenue"],
            total_cost=results["total_cost"],
            total_profit=results["total_profit"],
            profit_margin=results["profit_margin"],
            db_path=DB_PATH,
        )

        print("\nReport history saved.")

        # ====================================================
        # 14. COMPLETE
        # ====================================================

        print("\n================================")
        print("REPORTING PROCESS COMPLETED")
        print("================================")

        return results

    except Exception as error:

        # ====================================================
        # SAVE FAILURE HISTORY
        # ====================================================

        save_report_history(
            status="FAILED",
            error_message=str(error),
            db_path=DB_PATH,
        )

        print("\n================================")
        print("REPORTING PROCESS FAILED")
        print("================================")

        print(f"Error: {error}")

        # Re-raise the error so the scheduler
        # can also detect the failure.
        raise


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    main()
