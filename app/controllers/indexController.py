from util import db
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, current_user, login_required, logout_user
from emailHelper import send_mail
from forms import RegisterForm, LoginForm
from models import User
from datetime import datetime

# index page of the website
# GET method to render index page
# POST method is not supported
def index():
    return render_template('index.html')

# register page of the website
# GET method to render the register form
# POST method to submit the register form
#   redirect to index page with flash message if successful
#   redirect to register page with flash message if failed
def register():
    form = RegisterForm.RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User(
            username   = form.username.data,
            email      = form.email.data,
            password   = form.password.data,
            first_name = form.first_name.data,
            last_name  = form.last_name.data,
            role       = 'user',
            DOB        = form.BOD.data
        )

        # check that the username is used and confirmed
        user2 = User.User.query.filter_by(username=user.username).first()
        if user2 and user2.confirm:
            flash(f'This username ({user.username}) is already register', 'warning')
            return redirect(url_for('index.register'))

        # check that the email is used and confirmed
        user2 = User.User.query.filter_by(email=user.email).first()
        if user2 and user2.confirm:
            flash(f'This email ({user.email}) address is already register', 'warning')
            return redirect(url_for('index.register'))

        if not user2:
            db.session.add(user)
            db.session.commit()

        send_mail(recipients = [user.email],
                  subject    = 'Welcome to ...',
                  template   = 'mail/confirmRegistration',
                  user       = user,
                  token      = user.create_confirm_token(),
                 )

        flash(f'A confirmation email has been sent to {user.email}, please check your email inbox.', 'info')
        return redirect(url_for('index.index'))

    return render_template('register.html', form=form)

# FIXME: confirm register not working
def confirmRegistration(token):
    user = User.User()
    data = user.validate_confirm_token(token)

    if data > 0:
        user = User.User.query.filter_by(user_id=data.get('user_id')).first()
        user.confirm = True
        db.session.add(user)
        db.session.commit()

        send_mail(
            recipients = [user.email],
            subject    = 'Welcome to ...',
            template   = 'mail/registrationConfirmed',
            user       = user
        )

        flash(f'Your email address has been confirmed, thank you.', 'success')
        return redirect(url_for('index.login'))

# login page of the website
# GET method to render the login form
# POST method to submit the login form
#   redirect to index page with flash message if successful
#   redirect to login page with flash message if failed
def login():
    form = LoginForm.LoginForm()

    # check if the user is already logged in
    if request.method == 'GET' and current_user.is_authenticated:
        flash(f'Login successful!', 'success')
        return redirect(url_for('index.index'))

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            user.last_login = datetime.now
            db.session.commit()
            login_user(user, form.remember_me.data)
            flash(f'Login successful!', 'success')
            return redirect(url_for('index.index'))

        flash(f'Wrong username or password', 'warning')

    return render_template('login.html', form=form)

# logout function
# GET method to redirect to index page immediately
# POST method is not supported
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('index.index'))
