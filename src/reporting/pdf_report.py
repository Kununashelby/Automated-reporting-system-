import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)


def generate_pdf_report(results, output_path="reports/sales_report.pdf"):
    """
    Generate a professional PDF sales report.
    """

    # Create output directory
    output_dir = os.path.dirname(output_path)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # Create PDF document
    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    # Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=10,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=15,
        spaceAfter=10,
    )

    normal_style = styles["Normal"]

    # Story contains everything added to the PDF
    story = []

    # ==========================================
    # TITLE
    # ==========================================

    story.append(
        Paragraph(
            "Automated Sales Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Generated automatically by the Reporting System",
            normal_style,
        )
    )

    story.append(Spacer(1, 15))

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    story.append(
        Paragraph(
            "Executive Summary",
            heading_style,
        )
    )

    summary_data = [
        ["Metric", "Value"],
        [
            "Total Revenue",
            f"KSh {results['total_revenue']:,.2f}",
        ],
        [
            "Total Cost",
            f"KSh {results['total_cost']:,.2f}",
        ],
        [
            "Total Profit",
            f"KSh {results['total_profit']:,.2f}",
        ],
        [
            "Profit Margin",
            f"{results['profit_margin']:.2f}%",
        ],
        [
            "Units Sold",
            f"{results['total_units']:,}",
        ],
        [
            "Transactions",
            f"{results['transactions']:,}",
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[80 * mm, 70 * mm],
    )

    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(summary_table)

    story.append(Spacer(1, 15))

    # ==========================================
    # SALES BY PRODUCT
    # ==========================================

    story.append(
        Paragraph(
            "Sales by Product",
            heading_style,
        )
    )

    product_data = [["Product", "Revenue"]]

    for product, revenue in results["sales_by_product"].items():
        product_data.append(
            [
                product,
                f"KSh {revenue:,.2f}",
            ]
        )

    product_table = Table(
        product_data,
        colWidths=[80 * mm, 70 * mm],
    )

    product_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(product_table)

    # ==========================================
    # SALES BY CATEGORY
    # ==========================================

    story.append(
        Paragraph(
            "Sales by Category",
            heading_style,
        )
    )

    category_data = [["Category", "Revenue"]]

    for category, revenue in results["sales_by_category"].items():
        category_data.append(
            [
                category,
                f"KSh {revenue:,.2f}",
            ]
        )

    category_table = Table(
        category_data,
        colWidths=[80 * mm, 70 * mm],
    )

    category_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(category_table)

    # ==========================================
    # CHARTS
    # ==========================================

    story.append(PageBreak())

    story.append(
        Paragraph(
            "Sales Charts",
            heading_style,
        )
    )

    chart_paths = [
        "reports/charts/sales_by_product.png",
        "reports/charts/sales_by_category.png",
        "reports/charts/revenue_cost_profit.png",
    ]

    for chart_path in chart_paths:

        if os.path.exists(chart_path):

            image = Image(chart_path)

            image.drawHeight = 80 * mm
            image.drawWidth = 150 * mm

            story.append(image)
            story.append(Spacer(1, 10)) 

    # ==========================================
    # GENERATE PDF
    # ==========================================

    document.build(story)

    return output_path