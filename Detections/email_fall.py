import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
from flask import jsonify
import cv2
def SendMail(ImgFileName, user_email):
    try:
        img_data = open(ImgFileName, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'Fall Alert'
        msg['From'] = 'email.cc'
        msg['To'] = user_email

        text = MIMEText("Fall Detected. Send HELP")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
        msg.attach(image)

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login("email", "password")
        s.sendmail("email", user_email, msg.as_string())
        s.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

