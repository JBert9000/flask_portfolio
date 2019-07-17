from email.mime.text import MIMEText
import smtplib
# from imaplib import IMAP4


def send_email(email,height,average_height,count):
    from_email="testemail.python@yandex.com"
    from_password="testPython"
    to_email=email
    average_height=average_height
    count=count

    subject="Height Data"

    message="Hey there, your height is <strong>%s</strong>. Average height for everyone is: <strong>%s</strong>. <br> This program has collected height from <strong>%s</strong> people" % (height,average_height,count)

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    yandex=smtplib.SMTP('smtp.yandex.com',587)
    # yandex=imaplib.IMAP4("imap.yandex.com",993)

    yandex.ehlo()
    yandex.starttls()
    yandex.ehlo()
    yandex.login(from_email,from_password)
    yandex.send_message(msg)
