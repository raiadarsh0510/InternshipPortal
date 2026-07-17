import os
import smtplib
from email.message import EmailMessage

from email_validator import validate_email, EmailNotValidError
from flask import current_app, url_for
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer


def _get_serializer():
    return URLSafeTimedSerializer(current_app.secret_key)


def generate_verification_token(email: str) -> str:
    serializer = _get_serializer()
    return serializer.dumps(email, salt="email-verification-salt")


def confirm_verification_token(token: str, expiration_seconds: int = 86400) -> str:
    serializer = _get_serializer()
    return serializer.loads(
        token,
        salt="email-verification-salt",
        max_age=expiration_seconds
    )


def send_email(subject: str, recipient: str, body: str, html_body: str = None) -> bool:
    try:
        validated = validate_email(recipient)
        recipient_address = validated.email
    except EmailNotValidError:
        current_app.logger.warning(
            "Invalid email address for sending mail: %s",
            recipient
        )
        return False

    sender = current_app.config.get("MAIL_DEFAULT_SENDER")
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient_address
    message.set_content(body)

    if html_body:
        message.add_alternative(html_body, subtype="html")

    mail_server = current_app.config.get("MAIL_SERVER")
    mail_port = current_app.config.get("MAIL_PORT", 587)
    mail_username = current_app.config.get("MAIL_USERNAME")
    mail_password = current_app.config.get("MAIL_PASSWORD")
    use_tls = current_app.config.get("MAIL_USE_TLS", True)

    if not mail_server or not mail_username or not mail_password:
        current_app.logger.info(
            "Email not sent because SMTP settings are incomplete. Subject: %s Recipient: %s",
            subject,
            recipient_address,
        )
        current_app.logger.info("Email body:\n%s", body)
        return False

    try:
        with smtplib.SMTP(mail_server, mail_port, timeout=10) as smtp:
            if use_tls:
                smtp.starttls()
            smtp.login(mail_username, mail_password)
            smtp.send_message(message)

        return True
    except Exception as exc:
        current_app.logger.warning(
            "Failed to send email to %s: %s",
            recipient_address,
            exc,
        )
        return False


def send_verification_email(user) -> bool:
    token = generate_verification_token(user.email)
    verify_url = url_for(
        "verify_email",
        token=token,
        _external=True
    )
    subject = "Verify your SRDT Internship Portal account"
    body = f"Hi {user.name},\n\nPlease verify your email address by clicking the link below:\n\n{verify_url}\n\nIf you did not register, please ignore this message.\n\nThank you!"
    html_body = (
        f"<p>Hi {user.name},</p>"
        f"<p>Please verify your email address by clicking the link below:</p>"
        f"<p><a href=\"{verify_url}\">Verify My Email</a></p>"
        f"<p>If you did not register, please ignore this message.</p>"
        f"<p>Thank you!</p>"
    )
    return send_email(subject, user.email, body, html_body)
