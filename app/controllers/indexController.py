from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, logout_user
from datetime import datetime
from app.emailHelper import send_mail



# index page of the website
# GET method to render index page
# POST method for search function
def index():
    categories  = ProductCategory.getAll()
    searchFrom = SearchForm()

    # Search
    if request.method == 'POST' and form_search.validate_on_submit():
        words = form_search.search.data.split(' ')

        products_list = list()
        for word in words:
            products_list.extend(Product.query.filter(Product.name.contains(word)).all())
            products_list.extend(Product.query.filter(Product.description.contains(word)).all())
        products = set(products_list)

    else:
        products = Product.getAll()

    return render_template('index.html',
                            searchFrom = searchFrom,
                            categories = categories,
                            products   = products
                        )



# register page of the website
# GET method to render the register form
# POST method to submit the register form
#   redirect to index page with flash message if successful
#   redirect to register page with flash message if failed
def register():
    registerForm = RegisterForm()

    if request.method == 'POST' and registerForm.validate_on_submit():
        # check that the username is used and confirmed
        userCheck = User.getByUsername(registerForm.username.data)
        if userCheck and userCheck.confirm:
            flash(f'This username ({registerForm.username.data}) is already register', 'warning')
            return redirect(url_for('index.register'))

        # check that the email is used and confirmed
        userCheck = User.getByEmail(registerForm.email.data)
        if userCheck and userCheck.confirm:
            flash(f'This email ({registerForm.email.data}) address is already register', 'warning')
            return redirect(url_for('index.register'))

        if userCheck and userCheck.confirm == False:
            customer = userCheck

        elif not userCheck:
            customer = Customer.create(
                            username   = registerForm.username.data,
                            email      = registerForm.email.data,
                            password   = registerForm.password.data,
                            first_name = registerForm.first_name.data,
                            last_name  = registerForm.last_name.data,
                            DOB        = registerForm.DOB.data
                        )

        send_mail(recipients = [customer.email],
                  subject    = 'Welcome to ...',
                  template   = 'mail/confirmRegistration',
                  user       = customer,
                  token      = customer.create_confirm_token(),
                 )

        flash(f'A confirmation email has been sent to {customer.email}, please check your email inbox.', 'info')
        return redirect(url_for('index.index'))

    return render_template('register.html', registerForm=registerForm)



# confirm registration function
# GET method to validate confirmation token
#   :param: token
# POST method is not allowed
def confirmRegistration(token):
    customer = Customer()
    data = customer.validate_confirm_token(token)

    if data is None:
        flash(f'You confirmation link is invalid or expired, please try again.', 'danger')

    else:
        customer = Customer.getByID(data.get('user_id'))
        customer.updateConfirm()

        send_mail(recipients = [customer.email],
                  subject    = 'Welcome to ...',
                  template   = 'mail/registrationConfirmed',
                  user       = customer
                 )

        flash(f'Your email address has been confirmed, thank you.', 'success')
    return redirect(url_for('index.login'))



# login page of the website
# GET method to render the login form
# POST method to submit the login form
#   redirect to index page with flash message if successful
#   redirect to login page with flash message if failed
def login():
    form = LoginForm()

    # check if the user is already logged in
    if request.method == 'GET' and current_user.is_authenticated:
        flash(f'Login successful!', 'success')
        return redirect(url_for('index.index'))

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            user.last_login = datetime.now()
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
    form = ForgotPasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.confirm == True:
            send_mail(recipients = [user.email],
                      subject    = 'Reset your password',
                      template   = 'mail/resetPassword',
                      user       = user,
                      token      = user.create_confirm_token()
                     )

        flash(f'A reset password email has been sent to your email if your email is registered.', 'success')
        return redirect(url_for('index.index'))

    return render_template('forgotPassword.html', form=form)



# reset password function
# GET method to render reset password form
# :param: token
# POST method to submit the reset password form
def resetPassword(token):
    form = ResetPasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User()
        data = user.validate_confirm_token(token)

        if data is None:
            flash(f'You link is invalid or expired, please try again.', 'danger')
            return redirect(url_for('index.index'))

        user = User.query.filter_by(user_id=data.get('user_id')).first()
        user.password = form.password.data

        send_mail(recipients = [user.email],
                  subject    = 'Password Updated Successfully',
                  template   = 'mail/passwordUpdated',
                  user       = user
                 )

        flash(f'Your password has been updated.', 'success')
        return redirect(url_for('index.login'))

    return render_template('resetPassword.html', form=form)
