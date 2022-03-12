import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def new_user_mail(username, email, full_name):

    subject = "New account created"
    text = f"""Your account has been created:
    
    Username - {username}
    Full Name - {full_name}
    Email - {email}
    
    Thank you for your support."""

    msg = MIMEMultipart()
    msg["From"] = "Booking-search-engine"
    send_to = email
    sender = 'booking.search.engine@gmail.com'
    msg["Date"] =  datetime.datetime.now().strftime("%d-%m-%Y")
    msg["Subject"] = subject
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(sender, 'Secret12345')
    smtp.sendmail(sender, send_to, msg.as_string())
    smtp.close()

def reservation_mail(receiver):

    msg = MIMEMultipart()
    send_to = receiver
    sender = 'booking.search.engine@gmail.com'

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(sender, 'Secret12345')
    smtp.sendmail(sender, send_to, msg.as_string())
    smtp.close()