from src.reporting.pdf_report import generate_pdf_report
from src.reporting.data_loader import load_csv
from src.reporting.analyzer import analyze_sales
from src.reporting.charts import (
    sales_by_product,
    sales_by_category,
    revenue_cost_profit,
)


def main():
    # ==============================
    # 1. LOAD SALES DATA
    # ==============================
    data = load_csv("data/sample_sales.csv")

    # ==============================
    # 2. ANALYZE SALES DATA
    # ==============================
    results = analyze_sales(data)

    # ==============================
    # 3. DISPLAY SALES REPORT
    # ==============================
    print("\n===== SALES REPORT =====")

    print(f"Total Revenue: KSh {results['total_revenue']:,.2f}")
    print(f"Total Cost: KSh {results['total_cost']:,.2f}")
    print(f"Total Profit: KSh {results['total_profit']:,.2f}")
    print(f"Profit Margin: {results['profit_margin']:.2f}%")
    print(f"Units Sold: {results['total_units']}")
    print(f"Transactions: {results['transactions']}")

    # ==============================
    # 4. SALES BY PRODUCT
    # ==============================
    print("\n===== SALES BY PRODUCT =====")

    for product, revenue in results["sales_by_product"].items():
        print(f"{product}: KSh {revenue:,.2f}")

    # ==============================
    # 5. SALES BY CATEGORY
    # ==============================
    print("\n===== SALES BY CATEGORY =====")

    for category, revenue in results["sales_by_category"].items():
        print(f"{category}: KSh {revenue:,.2f}")

    # ==============================
    # 6. GENERATE CHARTS
    # ==============================
    print("\n===== GENERATING CHARTS =====")

    product_chart = sales_by_product(results["data"])
    print(f"Product chart: {product_chart}")

    category_chart = sales_by_category(results["data"])
    print(f"Category chart: {category_chart}")

    profit_chart = revenue_cost_profit(results["data"])
    print(f"Revenue/Cost/Profit chart: {profit_chart}")

    print("\nCharts generated successfully.")

        # ==============================
    # 7. GENERATE PDF REPORT
    # ==============================

    print("\n===== GENERATING PDF REPORT =====")

    pdf_path = generate_pdf_report(results)

    print(f"PDF report: {pdf_path}")
    print("\nPDF report generated successfully.")


# ==============================
# APPLICATION ENTRY POINT
# ==============================
if __name__ == "__main__":
    main()
