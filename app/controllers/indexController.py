from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from app.email_helper import send_mail



# index page of the website
# GET method to render index page
# POST method for search function
def index():
    categories = ProductCategory.getAll(True)
    searchForm = SearchForm()

    # Search
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        products_list = list()
        for word in words:
            products_list.extend(Product.getAllJoinedProductContains(word, True))
        products = set(products_list)

    else: products = Product.getAllJoinedProduct(True)

    categoryCount = {category.category_id: Product.countProductByCategory(category.category_id, True) for category in categories}
    categoryCount[0] = Product.count(True)

    return render_template('index.html',
                            searchForm    = searchForm,
                            categories    = categories,
                            categoryCount = categoryCount,
                            products      = products
                        )



def filterIndex(category_id):
    categories = ProductCategory.getAll(True)
    searchForm = SearchForm()

    # Search
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        products_list = list()
        for word in words:
            products_list.extend(Product.getAllJoinedProductByCategoryIDContains(category_id, word, True))
            products_list.extend(Product.getAllJoinedProductByCategoryIDContains(category_id, word, True))
        products = set(products_list)

    else: products = Product.getAllJoinedProductByCategoryID(category_id, True)

    categoryCount = {category.category_id: Product.countProductByCategory(category.category_id, True) for category in categories}
    categoryCount[0] = Product.count(True)

    return render_template('index.html',
                            searchForm    = searchForm,
                            categories    = categories,
                            categoryCount = categoryCount,
                            products      = products,
                            filter        = category_id,
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
        if userCheck and userCheck.is_active:
            flash(f'This username ({registerForm.username.data}) is already register', 'warning')
            return redirect(url_for('index.register'))

        # check that the email is used and confirmed
        userCheck = User.getByEmail(registerForm.email.data)
        if userCheck and userCheck.is_active:
            flash(f'This email ({registerForm.email.data}) address is already register', 'warning')
            return redirect(url_for('index.register'))

        if userCheck and userCheck.is_active == False:
            customer = userCheck

        elif not userCheck:
            customer = Customer.create(
                            username   = registerForm.username.data,
                            email      = registerForm.email.data,
                            password   = registerForm.password.data,
                            first_name = registerForm.first_name.data,
                            last_name  = registerForm.last_name.data,
                            DOB        = registerForm.dob.data
                        )

        send_mail(recipients = [customer.email],
                  subject    = '[Moonbird] Welcome to Moonbird!',
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
        customer.update(is_active=True)

        send_mail(recipients = [customer.email],
                  subject    = '[Moonbird] Your account has been confirmed!',
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
            if user.is_active:
                user.last_login = datetime.now()
                user.update()
                login_user(user, form.remember_me.data)
                flash(f'Login successful!', 'success')

            else:
                flash(f'Your account is inactive.', 'warning')

            return redirect(url_for('index.index'))

        else:
            flash(f'Wrong username or password', 'warning')
            return redirect(url_for('index.login'))

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
        if user is not None and user.is_active == True:
            send_mail(recipients = [user.email],
                      subject    = '[Moonbird] Reset your password',
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
                  subject    = '[Moonbird] Password Updated Successfully',
                  template   = 'mail/passwordUpdated',
                  user       = user
                 )

        flash(f'Your password has been updated.', 'success')
        return redirect(url_for('index.login'))

    return render_template('resetPassword.html', form=form)



@login_required
def shoppingCart(user_id):
    if current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    flag = 1
    orderDiscount = None
    redeemCodeForm = RedeemCodeForm()
    if request.method == 'POST' and redeemCodeForm.validate_on_submit():
        flag = 0
        orderDiscount = OrderDiscount.getByCode(redeemCodeForm.code.data)
        if orderDiscount is None:
            flash(f'Promo Code not found', 'warning')

    items = CartItem.getAllJoinedItems(user_id)

    quantity = 0
    amount = 0
    for item in items:
        quantity += item.quantity
        if item.discountPercentage:
            amount += item.amount * (1-item.discountPercentage/100)
        else:
            amount += item.amount

    shippingDiscount = ShippingDiscount.getActive()
    addresses = CustomerAddress.getAllByID(user_id)

    user = User.getByID(user_id)
    checkoutForm = CheckoutForm(addresses)
    if request.method == 'POST' and flag and checkoutForm.validate_on_submit():
        if shippingDiscount is not None and amount >shippingDiscount.atLeastAmount:
            shippingFee = 0
        else:
            shippingFee = round(amount*0.05, 2)

        amount += shippingFee
        if orderDiscount:
            amount *= (1- orderDiscount.discountPercentage/100)

        if checkoutForm.paymentType.data == 'Credit':
            if checkoutForm.CreditCardNumber.data == '' or \
                checkoutForm.Expiration.data == '' or \
                checkoutForm.CVV.data == '':
                flash(f'You must provide your credit card information', 'warning')
                return redirect(url_for('index.shoppingCart', user_id=user_id))

            if Order.create(
                    customer_id = user_id,
                    address_id = checkoutForm.addresses.data,
                    order_discount = orderDiscount,
                    items = items,
                    amount = amount,
                    shippingFee = shippingFee,
                    payment_type = 'Credit',
                    account_no = checkoutForm.CreditCardNumber.data
                ):
                flash(f'Order created successfully!', 'success')

                send_mail(recipients = [user.email],
                          subject    = '[Moonbird] Your Order have been accepted and now being processed!',
                          template   = 'mail/checkout',
                          user       = user
                         )

                for item in items:
                    p = Product.getByID(item.product_id)
                    p.sell(item.quantity)
                    i = CartItem.getByID(item.cart_id, item.product_id)
                    i.remove()

                return redirect(url_for('index.index'))

            flash(f'Order created failed!', 'warning')
            return redirect(url_for('index.shoppingCart', user_id=user_id))

        elif checkoutForm.paymentType.data == 'Cash':
            if Order.create(
                    customer_id = user_id,
                    address_id = checkoutForm.addresses.data,
                    order_discount = orderDiscount,
                    items = items,
                    amount = amount,
                    shippingFee = shippingFee
                ):
                flash(f'Order created successfully!', 'success')

                send_mail(recipients = [user.email],
                          subject    = '[Moonbird] Your Order have been accepted and now being processed!',
                          template   = 'mail/checkout',
                          user       = user
                         )

                for item in items:
                    p = Product.getByID(item.product_id)
                    p.sell(item.quantity)
                    i = CartItem.getByID(item.cart_id, item.product_id)
                    i.remove()

                return redirect(url_for('index.index'))

            flash(f'Order created failed!', 'warning')
            return redirect(url_for('index.shoppingCart', user_id=user_id))

        else:
            flash(f'Order created failed!', 'warning')
            return redirect(url_for('index.shoppingCart', user_id=user_id))

    checkoutForm.init()
    return render_template('shoppingCart.html',
                            items            = items,
                            quantity         = quantity,
                            amount           = amount,
                            user_id          = user_id,
                            addresses        = addresses,
                            redeemCodeForm   = redeemCodeForm,
                            checkoutForm     = checkoutForm,
                            shippingDiscount = shippingDiscount,
                            orderDiscount    = orderDiscount
                        )
