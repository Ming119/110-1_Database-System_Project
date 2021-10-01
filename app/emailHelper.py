from util import mail;
from flask import current_app, render_template;
from flask_mail import Message;
from threading import Thread;

def send_mail(recipients, subject, template, sender=None, mailtype='html', **kwargs):
    app = current_app._get_current_object();

    if not sender:
        sender = app.config.get('MAIL_USERNAME');

    msg = Message(subject, sender=sender, recipients=recipients);

    if mailtype == 'html':
        msg.html = render_template(template + '.html', **kwargs);
    elif mailtype == 'txt':
        msg.body = render_template(template + '.txt', **kwargs);
    elif mailtype == 'body':
        msg.body = template;

    thr = Thread(target=send_async_mail, args=[app, msg]);
    thr.start();

    return thr;

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg);
