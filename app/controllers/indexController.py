from util import db;
from flask import flash, redirect, render_template, request, session, url_for;
from flask_login import login_user, current_user, login_required, logout_user;
from emailHelper import send_mail;
from forms import RegisterForm, LoginForm;
from models import User, Adminuser;

def index():
    return render_template('index.html');



def register():
    form = RegisterForm.RegisterForm();

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User(
            username   = form.username.data,
            email      = form.email.data,
            password   = form.password.data,
            first_name = form.first_name.data,
            last_name  = form.last_name.data
        );

        db.session.add(user);
        db.session.commit();

        send_mail(recipients = [form.email.data],
                  subject    = 'Welcome to ...',
                  template   = 'mail/confirmRegistration',
                  user       = user,
                  token      = user.create_confirm_token(),
                 );

        flash(f'A confirmation email has been sent to {form.email.data}, please check your email inbox.', 'info');
        return redirect(url_for('index.index'));

    return render_template('register.html', form=form);



def confirmRegistration(token):
    user = User.User();
    data = user.validate_confirm_token(token);

    if data > 0:
        user = User.User.query.filter_by(user_id=data.get('user_id')).first();
        user.confirm = True;
        db.session.add(user);
        db.session.commit();

        send_mail(recipients = [user.email],
                  subject    = 'Welcome to ...',
                  template   = 'mail/registrationConfirmed',
                  user       = user
                 );

        flash(f'Your email address has been confirmed, thank you.', 'success');
        return redirect(url_for('index.login'));

    elif data == -1:
        user = User.User.query.filter_by(user_id=data.get('user_id')).first();

        send_mail(recipients = [user.email],
                  subject    = 'Welcome to ...',
                  template   = 'mail/confirmRegistration',
                  user       = user,
                  token      = user.create_confirm_token(),
                 );

        flash(f'Your confirmation link has been expired. A new confirmation link has been sent to your email address, please try again.', 'warning');
        return redirect(url_for('index.index'));

    elif data == -2:
        flash(f'Your confirmation link is incorrect.', 'danger');
        return redirect(url_for('index.index'));

def login():
    form = LoginForm.LoginForm();

    if request.method == 'GET' and current_user.is_authenticated:
        flash(f'Login successful!', 'success');
        return redirect(url_for('index.index'));

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User.query.filter_by(username=form.username.data).first();
        # if not user:
        #     user = Adminuser.Adminuser.query.filter_by(username=form.username.data).first();

        if user:
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data);
                flash(f'Login successful!', 'success');
                return redirect(url_for('index.index'));

        flash(f'Wrong username or password', 'warning');

    return render_template('login.html', form=form);



def logout():
    logout_user();
    flash('Logout successful!', 'success');
    return redirect(url_for('index.index'));
