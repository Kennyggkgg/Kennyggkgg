import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AlertSystem:
    def __init__(self, email_receiver, smtp_server="smtp.gmail.com", smtp_port=587):
        self.email_receiver = email_receiver
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email_alert(self, subject, message, email_sender, email_password):
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = self.email_receiver
        msg['Subject'] = subject

        # Add the message body
        body = MIMEText(message, 'plain')
        msg.attach(body)

        try:
            # Connect to the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Secure the connection
            server.login(email_sender, email_password)  # Login to the server
            server.sendmail(email_sender, self.email_receiver, msg.as_string())  # Send the email
            server.quit()  # Terminate the SMTP session
            print(f"Email sent to {self.email_receiver}!")
        except Exception as e:
            print(f"Failed to send email: {e}")