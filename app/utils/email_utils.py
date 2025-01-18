import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(recipient_email, subject, body):
    # Email details
    zoho_email = os.getenv("ZOHO_EMAIL")
    zoho_password =   os.getenv("ZOHO_EMAIL_PASSWORD")
    recipient_email = "dadaauthourity23@gmail.com"


    # Set up the MIME structure
    message = MIMEMultipart()
    message["From"] = f"Authority Innovations Hub <{zoho_email}>"
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach the HTML content
    message.attach(MIMEText(body, "html"))

    # Connect to Zoho SMTP server and send the email
    try:
        with smtplib.SMTP("smtp.zoho.com", 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(zoho_email, zoho_password)
            server.sendmail(zoho_email, recipient_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
