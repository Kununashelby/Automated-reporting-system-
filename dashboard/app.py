import os
import sys

import pandas as pd

from flask import (
    Flask,
    render_template,
    send_file,
    request,
)


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)


# --------------------------------------------------
# IMPORT REPORTING MODULES
# --------------------------------------------------

from src.reporting.database import (
    load_sales_from_database,
    load_report_history,
    load_settings,
    save_settings,
)

from src.reporting.analyzer import analyze_sales


# --------------------------------------------------
# FLASK APP
# --------------------------------------------------

app = Flask(__name__)


DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "reporting.db"
)

PDF_PATH = os.path.join(
    BASE_DIR,
    "reports",
    "sales_report.pdf"
)

EXCEL_PATH = os.path.join(
    BASE_DIR,
    "reports",
    "sales_report.xlsx"
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/")
def dashboard():

    data = load_sales_from_database(
        DB_PATH
    )

    results = analyze_sales(
        data
    )

    history = load_report_history(
        DB_PATH
    )

    sales_by_product = {
        product: float(revenue)
        for product, revenue
        in results["sales_by_product"].items()
    }

    sales_by_category = {
        category: float(revenue)
        for category, revenue
        in results["sales_by_category"].items()
    }

    return render_template(
        "dashboard.html",

        total_revenue=results[
            "total_revenue"
        ],

        total_cost=results[
            "total_cost"
        ],

        total_profit=results[
            "total_profit"
        ],

        profit_margin=results[
            "profit_margin"
        ],

        total_units=results[
            "total_units"
        ],

        transactions=results[
            "transactions"
        ],

        sales_by_product=sales_by_product,

        sales_by_category=sales_by_category,

        history=history.to_dict(
            orient="records"
        )
    )


# --------------------------------------------------
# REPORTS PAGE
# --------------------------------------------------

@app.route("/reports")
def reports():

    history = load_report_history(
        DB_PATH
    )

    return render_template(
        "reports.html",
        history=history.to_dict(
            orient="records"
        )
    )

# --------------------------------------------------
# REPORT HISTORY
# --------------------------------------------------

@app.route("/history")
def history():

    history_data = load_report_history(
        DB_PATH
    )

    total_runs = len(history_data)

    successful_runs = len(
        history_data[
            history_data["status"] == "SUCCESS"
        ]
    )

    failed_runs = len(
        history_data[
            history_data["status"] == "FAILED"
        ]
    )

    return render_template(
        "history.html",

        history=history_data.to_dict(
            orient="records"
        ),

        total_runs=total_runs,

        successful_runs=successful_runs,

        failed_runs=failed_runs
    )

# --------------------------------------------------
# SALES ANALYTICS
# --------------------------------------------------

@app.route("/sales")
def sales():

    data = load_sales_from_database(DB_PATH)

    # Convert date column to datetime
    data["date"] = pd.to_datetime(data["date"])

    # Get filter parameters
    period = request.args.get("period", "30")

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    today = pd.Timestamp.today().normalize()

    # Apply preset filters
    if period == "today":

        data = data[
            data["date"] == today
        ]

    elif period == "7":

        start = today - pd.Timedelta(days=6)

        data = data[
            (data["date"] >= start) &
            (data["date"] <= today)
        ]

    elif period == "30":

        start = today - pd.Timedelta(days=29)

        data = data[
            (data["date"] >= start) &
            (data["date"] <= today)
        ]

    elif period == "month":

        start = today.replace(day=1)

        data = data[
            (data["date"] >= start) &
            (data["date"] <= today)
        ]

    elif period == "custom" and start_date and end_date:

        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)

        data = data[
            (data["date"] >= start) &
            (data["date"] <= end)
        ]

    # Handle empty filtered results
    if data.empty:

        return render_template(
            "sales.html",

            total_revenue=0,
            total_profit=0,
            total_units=0,
            transactions=0,

            daily_labels=[],
            daily_values=[],

            product_data=[],
            category_data=[],
            sales_data=[],

            selected_period=period,
            selected_start=start_date or "",
            selected_end=end_date or ""
        )

    # Calculate revenue
    data["revenue"] = (
        data["quantity"] *
        data["price"]
    )

    data["total_cost"] = (
        data["quantity"] *
        data["cost"]
    )

    data["profit"] = (
        data["revenue"] -
        data["total_cost"]
    )

    total_revenue = data["revenue"].sum()
    total_profit = data["profit"].sum()
    total_units = data["quantity"].sum()
    transactions = len(data)

    # Daily sales
    daily_sales = (
        data.groupby("date")["revenue"]
        .sum()
        .sort_index()
    )

    # Product performance
    product_data = (
        data.groupby("product")
        .agg(
            revenue=("revenue", "sum"),
            units=("quantity", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    # Category performance
    category_data = (
        data.groupby("category")
        .agg(
            revenue=("revenue", "sum"),
            units=("quantity", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    # Convert dates back to strings for HTML
    data["date"] = data["date"].dt.strftime(
        "%Y-%m-%d"
    )

    return render_template(
        "sales.html",

        total_revenue=total_revenue,
        total_profit=total_profit,
        total_units=total_units,
        transactions=transactions,

        daily_labels=[
            date.strftime("%Y-%m-%d")
            for date in daily_sales.index
        ],

        daily_values=[
            float(value)
            for value in daily_sales.values
        ],

        product_data=[
            {
                "product": product,
                "revenue": float(row["revenue"]),
                "units": int(row["units"]),
                "profit": float(row["profit"]),
            }

            for product, row
            in product_data.iterrows()
        ],

        category_data=[
            {
                "category": category,
                "revenue": float(row["revenue"]),
                "units": int(row["units"]),
                "profit": float(row["profit"]),
            }

            for category, row
            in category_data.iterrows()
        ],

        sales_data=data.to_dict(
            orient="records"
        ),

        selected_period=period,
        selected_start=start_date or "",
        selected_end=end_date or ""
    )

# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

@app.route("/settings", methods=["GET", "POST"])
def settings():

    if request.method == "POST":

        new_settings = {
            "report_time": request.form.get(
                "report_time",
                "18:00"
            ),

            "report_format": request.form.get(
                "report_format",
                "both"
            ),

            "email_enabled": request.form.get(
                "email_enabled",
                "yes"
            ),

            "currency": request.form.get(
                "currency",
                "KSh"
            ),
        }

        save_settings(
            new_settings,
            DB_PATH
        )

    current_settings = load_settings(
        DB_PATH
    )

    return render_template(
        "settings.html",
        settings=current_settings
    )

# --------------------------------------------------
# DOWNLOAD PDF
# --------------------------------------------------

@app.route("/download/pdf")
def download_pdf():

    if not os.path.exists(PDF_PATH):
        return (
            "PDF report not found. "
            "Run the reporting system first."
        ), 404

    return send_file(
        PDF_PATH,
        as_attachment=True,
        download_name="sales_report.pdf"
    )


# --------------------------------------------------
# DOWNLOAD EXCEL
# --------------------------------------------------

@app.route("/download/excel")
def download_excel():

    if not os.path.exists(EXCEL_PATH):
        return (
            "Excel report not found. "
            "Run the reporting system first."
        ), 404

    return send_file(
        EXCEL_PATH,
        as_attachment=True,
        download_name="sales_report.xlsx"
    )


# --------------------------------------------------
# START SERVER
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
