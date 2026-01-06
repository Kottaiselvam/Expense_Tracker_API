"""
Report Service
Handles PDF report generation for expenses
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf_report(expenses):
    """
    Generate PDF report from expense list
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4
    y = height - 40

    # Title
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Expense Report")
    y -= 30

    # Header
    pdf.setFont("Helvetica-Bold", 10)
    headers = ["Date", "Category", "Amount", "Payment Mode"]
    x_positions = [40, 150, 280, 360]

    for i, header in enumerate(headers):
        pdf.drawString(x_positions[i], y, header)

    y -= 20
    pdf.setFont("Helvetica", 10)

    # Expense rows
    for exp in expenses:
        pdf.drawString(x_positions[0], y, str(exp["expense_date"]))
        pdf.drawString(x_positions[1], y, exp["category"])
        pdf.drawString(x_positions[2], y, str(exp["amount"]))
        pdf.drawString(x_positions[3], y, str(exp.get("payment_mode", "")))

        y -= 18

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = height - 40

    pdf.save()
    buffer.seek(0)
    return buffer
