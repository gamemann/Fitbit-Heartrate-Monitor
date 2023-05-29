import smtplib

def send_email(host="localhost", port=25, from_email="test@localhost", from_name="Fitbit Monitor", to_name="Test User", to_email="test@localhost", subject="Heartrate Threshold!", message="Test contents!"):
    smtp = smtplib.SMTP(host=host, port=port)
    
    body = """From: %s <%s>
        To: %s <%s>
        Subject: %s

        %s
    """ % (from_name, from_email, to_name, to_email, subject, message)

    try:
        smtp.sendmail(from_email, to_email, body)

    except smtplib.SMTPException as e:
        print("Error sending email %s to %s" % (from_email, to_email))
        print(e)
