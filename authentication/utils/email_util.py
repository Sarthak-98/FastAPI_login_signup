import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

email_username = os.getenv("EMAIL_USERNAME")
email_password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))

def send_email(user_data: str, subject: str, body: str):
        
    try:
        # Create a MIMEText object to represent the email content
        message = MIMEMultipart()
        message["From"] = email_username
        message["To"] = user_data
        message["Subject"] = subject

        # Attach the body of the email as a MIMEText object
        message.attach(MIMEText(body, "html"))        
        

        # Establish the connection to the SMTP server using TLS encryption
        server = smtplib.SMTP(smtp_server, smtp_port)
        # print(server)
        server.starttls()


        # Login to the email account
        server.login(email_username, email_password)

        # Send the email
        server.sendmail(email_username, user_data, message.as_string())

        # Close the connection to the server 
        server.quit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to send email")