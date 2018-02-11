from flask_mail import Message
from flask import render_template
from . import email

def send_email(subject,template,to,**kwargs):
    sender_email='vicky.mutai96@gmail.com'
    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    email.send(email)