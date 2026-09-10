import os

import matplotlib.pyplot as plt
import pandas as pd


def create_output_directory(output_dir: str) -> None:
    """Create the chart output directory if it doesn't exist."""
    os.makedirs(output_dir, exist_ok=True)


def sales_by_product(
    data: pd.DataFrame,
    output_dir: str = "reports/charts"
) -> str:
    """Create a bar chart showing revenue by product."""

    create_output_directory(output_dir)

    revenue = (
        data.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 6))

    revenue.plot(kind="bar")

    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue (KSh)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_path = os.path.join(output_dir, "sales_by_product.png")

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def sales_by_category(
    data: pd.DataFrame,
    output_dir: str = "reports/charts"
) -> str:
    """Create a bar chart showing revenue by category."""

    create_output_directory(output_dir)

    revenue = (
        data.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 6))

    revenue.plot(kind="bar")

    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue (KSh)")
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = os.path.join(output_dir, "sales_by_category.png")

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path


def revenue_cost_profit(
    data: pd.DataFrame,
    output_dir: str = "reports/charts"
) -> str:
    """Create a chart comparing revenue, cost and profit."""

    create_output_directory(output_dir)

    revenue = data["revenue"].sum()
    cost = data["total_cost"].sum()
    profit = data["profit"].sum()

    values = [revenue, cost, profit]
    labels = ["Revenue", "Cost", "Profit"]

    plt.figure(figsize=(8, 6))

    plt.bar(labels, values)

    plt.title("Revenue vs Cost vs Profit")
    plt.ylabel("Amount (KSh)")
    plt.tight_layout()

    output_path = os.path.join(
        output_dir,
        "revenue_cost_profit.png"
    )

    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path