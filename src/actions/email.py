import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

def send_email(host: str = "localhost", port: int = 25, from_email: str = "test@localhost", to_email: list[str] = ["test@localhost"], subject: str = "Heartrate Threshold!", message: str = "Test contents!"):
    smtp = smtplib.SMTP(host=host, port=port)

    for to in to_email:
        # Create MIME Multipart object.
        mime = MIMEMultipart("alternative")

        # Set the subject.
        mime["Subject"] = Header(subject, "utf-8")

        # Set from email.
        mime["From"] = from_email

        # Set to email.
        mime["To"] = to

        # Parse body as text/html and attach to our MIME object.
        body = MIMEText(message, 'html')
        mime.attach(body)

        # Attemp to send mail.
        try:
            smtp.sendmail(from_email, to_email, mime.as_string())
        except smtplib.SMTPException as e:
            print("Error sending email %s to %s" % (from_email, to))
            print(e)

    smtp.quit()
