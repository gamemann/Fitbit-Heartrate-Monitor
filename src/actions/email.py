import smtplib

def send_email(host: str = "localhost", port: int = 25, from_email: str = "test@localhost", from_name: str = "Fitbit Monitor", to_name: str = "Test User", to_email: str = "test@localhost", subject: str = "Heartrate Threshold!", message: str = "Test contents!"):
    smtp = smtplib.SMTP(host=host, port=port)
    
    body: str = """From: %s <%s>
        To: %s <%s>
        Subject: %s

        %s
    """ % (from_name, from_email, to_name, to_email, subject, message)

    try:
        smtp.sendmail(from_email, to_email, body)

    except smtplib.SMTPException as e:
        print("Error sending email %s to %s" % (from_email, to_email))
        print(e)
