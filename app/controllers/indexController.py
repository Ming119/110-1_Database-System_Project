from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, current_user, login_required, logout_user
from datetime import datetime
from app.emailHelper import send_mail
from app.models import User, Product, ProductCategory
from app.forms import (
    RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, Search
)

# index page of the website
# GET method to render index page
# POST method for search function
def index():
    categories  = ProductCategory.ProductCategory.query.all()
    form_search = Search.Search()

    # Search
    if request.method == 'POST' and form_search.validate_on_submit():
        words = form_search.search.data.split(' ')

        products_list = list()
        for word in words:
            products_list.append(Product.Product.query.filter(Product.Product.name.contains(word)).all())
            products_list.append(Product.Product.query.filter(Product.Product.description.contains(word)).all())
        products = set(products_list)

    else:
        products = Product.Product.query.all()

    return render_template('index.html',
                            form_search      = form_search,
                            categories       = categories,
                            products         = products
                        )

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
            DOB        = form.DOB.data
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
            user.create();

        send_mail(recipients = [user.email],
                  subject    = 'Welcome to ...',
                  template   = 'mail/confirmRegistration',
                  user       = user,
                  token      = user.create_confirm_token(),
                 )

        flash(f'A confirmation email has been sent to {user.email}, please check your email inbox.', 'info')
        return redirect(url_for('index.index'))

    return render_template('register.html', form=form)

# confirm registration function
# GET method to validate confirmation token
#   :param: token
# POST method is not allowed
def confirmRegistration(token):
    user = User.User()
    data = user.validate_confirm_token(token)

    if data is None:
        flash(f'You confirmation link is invalid or expired, please try again.', 'danger')

    else:
        user = User.User.query.filter_by(user_id=data.get('user_id')).first()
        user.confirm = True
        user.update()

        send_mail(recipients = [user.email],
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
            user.update()
            login_user(user, form.remember_me.data)
            flash(f'Login successful!', 'success')
            return redirect(url_for('index.index'))

        flash(f'Wrong username or password', 'warning')

    return render_template('login.html', form=form)

# logout function
# GET method to logout and redirect to index page immediately
# POST method is not allowed
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('index.index'))


# forgot password page of the website
# GET method to render the forgot password form
# POST method to submit the forgot password form and send a reset password email
def forgotPassword():
    form = ForgotPasswordForm.ForgotPasswordForm();

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User.query.filter_by(email=form.email.data).first()
        if user is not None and user.confirm == True:
            send_mail(recipients = [user.email],
                      subject    = 'Reset your password',
                      template   = 'mail/resetPassword',
                      user       = user,
                      token      = user.create_confirm_token()
                     )

        flash(f'A reset password email has been sent to your email if your email is registered.', 'success')
        return redirect(url_for('index.index'));

    return render_template('forgotPassword.html', form=form)

# reset password function
# GET method to render reset password form
# :param: token
# POST method to submit the reset password form
def resetPassword(token):
    form = ResetPasswordForm.ResetPasswordForm();

    if request.method == 'POST' and form.validate_on_submit():
        user = User.User()
        data = user.validate_confirm_token(token)

        if data is None:
            flash(f'You link is invalid or expired, please try again.', 'danger')
            return redirect(url_for('index.index'));

        user = User.User.query.filter_by(user_id=data.get('user_id')).first()
        user.password = form.password.data

        send_mail(recipients = [user.email],
                  subject    = 'Password Updated Successfully',
                  template   = 'mail/passwordUpdated',
                  user       = user
                 )

        flash(f'Your password has been updated.', 'success')
        return redirect(url_for('index.login'));

    return render_template('resetPassword.html', form=form)
