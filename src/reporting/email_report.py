import os
import smtplib

from email.message import EmailMessage


def send_report_email(
    sender_email,
    sender_password,
    recipient_email,
    subject,
    body,
    attachments=None,
    smtp_server="smtp.gmail.com",
    smtp_port=465,
):
    """
    Send an email with optional report attachments.
    """

    message = EmailMessage()

    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.set_content(body)

    if attachments:
        for file_path in attachments:

            if not os.path.exists(file_path):
                raise FileNotFoundError(
                    f"Attachment not found: {file_path}"
                )

            with open(file_path, "rb") as file:

                file_data = file.read()

                file_name = os.path.basename(file_path)

            message.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=file_name,
            )

    with smtplib.SMTP_SSL(
        smtp_server,
        smtp_port
    ) as server:

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(message)

    return True