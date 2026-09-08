from src.reporting.data_loader import load_csv
from src.reporting.analyzer import analyze_sales


def main():
    # Load sales data
    data = load_csv("data/sample_sales.csv")

    # Analyze sales
    results = analyze_sales(data)

    # Display results
    print("\n===== SALES REPORT =====")

    print(f"Total Revenue: KSh {results['total_revenue']:,.2f}")
    print(f"Total Cost: KSh {results['total_cost']:,.2f}")
    print(f"Total Profit: KSh {results['total_profit']:,.2f}")
    print(f"Profit Margin: {results['profit_margin']:.2f}%")
    print(f"Units Sold: {results['total_units']}")
    print(f"Transactions: {results['transactions']}")

    print("\n===== SALES BY PRODUCT =====")

    for product, revenue in results["sales_by_product"].items():
        print(f"{product}: KSh {revenue:,.2f}")

    print("\n===== SALES BY CATEGORY =====")

    for category, revenue in results["sales_by_category"].items():
        print(f"{category}: KSh {revenue:,.2f}")


if __name__ == "__main__":
    main()
