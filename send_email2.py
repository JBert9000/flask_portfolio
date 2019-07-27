from email.mime.text import MIMEText
import smtplib
# from imaplib import IMAP4


def send_email(email):
    from_email="testemail.python@yandex.com"
    from_password="testPython"
    to_email=email
    # score=score
    # count=count

    subject="Tetris Scores via Jan Bertlik Website"

    message="Hey there, your score is <strong>%s</strong>. s people played Tetris on my site." % (email)

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    yandex=smtplib.SMTP('smtp.yandex.com',587)
    # yandex=imaplib.IMAP4("imap.yandex.com",993)

    yandex.ehlo()
    yandex.starttls()
    yandex.ehlo()
    # yandex.starttls()
    yandex.login(from_email,from_password)
    yandex.send_message(msg)
