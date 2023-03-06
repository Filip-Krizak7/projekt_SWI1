import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import schemas

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
    smtp.login(sender, 'jybovowcxaaizonx')
    smtp.sendmail(sender, send_to, msg.as_string())
    smtp.close()

def reservation_mail(receiver: schemas.User, name: str, address: str, price: int, roomType: str, persons: int, checkIn: str, checkOut: str):
    msg = MIMEMultipart()
    send_to = receiver.email
    sender = 'booking.search.engine@gmail.com'

    subject = "New reservation"
    text = f"""Thank you for creating a new reservation:
    
    Full Name - {receiver.full_name}
    Name of the hotel: {name}
    Address of the hotel: {address}
    Price: {price}
    Room type: {roomType}
    Number of persons: {persons}
    Check In Date: {checkIn}
    Check Out Date: {checkOut}
    
    Thank you for your support."""

    msg["From"] = "Booking-search-engine"
    msg["Date"] =  datetime.datetime.now().strftime("%d-%m-%Y")
    msg["Subject"] = subject
    msg.attach(MIMEText(text))

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(sender, 'jybovowcxaaizonx')
    smtp.sendmail(sender, send_to, msg.as_string())
    smtp.close()