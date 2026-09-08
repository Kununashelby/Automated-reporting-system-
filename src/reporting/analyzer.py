import pandas as pd


def analyze_sales(data: pd.DataFrame) -> dict:
    """
    Analyze sales data and return key business metrics.
    """

    required_columns = {
        "date",
        "product",
        "category",
        "quantity",
        "price",
        "cost",
    }

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    # Make a copy so the original DataFrame is not modified
    data = data.copy()

    # Calculate revenue and cost
    data["revenue"] = data["quantity"] * data["price"]
    data["total_cost"] = data["quantity"] * data["cost"]

    # Calculate profit
    data["profit"] = data["revenue"] - data["total_cost"]

    # Overall metrics
    total_revenue = data["revenue"].sum()
    total_cost = data["total_cost"].sum()
    total_profit = data["profit"].sum()
    total_units = data["quantity"].sum()
    transactions = len(data)

    # Profit margin
    if total_revenue > 0:
        profit_margin = (total_profit / total_revenue) * 100
    else:
        profit_margin = 0

    # Sales by product
    sales_by_product = (
        data.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    # Sales by category
    sales_by_category = (
        data.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    # Return results
    return {
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "total_profit": total_profit,
        "profit_margin": profit_margin,
        "total_units": total_units,
        "transactions": transactions,
        "sales_by_product": sales_by_product,
        "sales_by_category": sales_by_category,
        "data": data,
    }
