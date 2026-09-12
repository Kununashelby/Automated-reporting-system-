import os

from dotenv import load_dotenv

from src.reporting.email_report import send_report_email


load_dotenv()


sender_email = os.getenv("EMAIL_ADDRESS")
sender_password = os.getenv("EMAIL_PASSWORD")
recipient_email = os.getenv("REPORT_RECIPIENT")


send_report_email(
    sender_email=sender_email,
    sender_password=sender_password,
    recipient_email=recipient_email,
    subject="Automated Sales Report Test",
    body="""
Hello,

This is a test email from the Automated Reporting System.

The email delivery system is working correctly.

Regards,
Automated Reporting System
""",
)


print("Email sent successfully.")