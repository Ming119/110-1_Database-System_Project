from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.email_helper import send_mail


@login_required
def index(user_id):
    if current_user.role != 'staff' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    searchForm = SearchForm()
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        orders_list = list()
        for word in words:
            orders_list.extend(Order.getAllContains(word))
        orders = set(orders_list)

    elif current_user.role == 'staff':
        orders = Order.getAll()
    else:
        orders = Order.getByCustomerID(user_id)

    if current_user.role == 'staff':
        orderCount = {'all': Order.count(),
                        'processing': Order.count(status='processing'),
                        'delivering': Order.count(status='delivering'),
                        'delivered': Order.count(status='delivered'),
                    }
    else:
        orderCount = {'all': Order.count(user_id),
                        'processing': Order.count(status='processing', customer_id=user_id),
                        'delivering': Order.count(status='delivering', customer_id=user_id),
                        'delivered': Order.count(status='delivered', customer_id=user_id),
                    }

    return render_template('order/manageOrder.html',
                            searchForm = searchForm,
                            orders     = orders,
                            orderCount = orderCount,
                        )


@login_required
def filterIndex(user_id, status):
    if current_user.role != 'staff' and current_user.user_id != user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    searchForm = SearchForm()
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        orders_list = list()
        for word in words:
            orders_list.extend(Order.getAllContains(word))
        orders = set(orders_list)

    elif current_user.role == 'staff':
        orders = Order.getByStatus(status)
    else:
        orders = Order.getByCustomerID(user_id, status)

    if current_user.role == 'staff':
        orderCount = {'all': Order.count(),
                        'processing': Order.count('processing'),
                        'delivering': Order.count('delivering'),
                        'delivered': Order.count('delivered'),
                    }
    else:
        orderCount = {'all': Order.count(user_id),
                        'processing': Order.count('processing', user_id),
                        'delivering': Order.count('delivering', user_id),
                        'delivered': Order.count('delivered', user_id),
                    }

    return render_template('order/manageOrder.html',
                            searchForm = searchForm,
                            orders     = orders,
                            orderCount = orderCount,
                            filter     = status
                        )



@login_required
def details(order_id):
    order = Order.getByID(order_id)
    if current_user.role != 'staff' and current_user.user_id != order.Customer.user_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))


    commentForm = CommentForm()
    if request.method == 'POST' and commentForm.validate_on_submit():
        if Comment.create(
            product_id = commentForm.product_id.data,
            user_id    = order.Customer.user_id,
            comment    = commentForm.comment.data,
            rating     = commentForm.score.data
        ):
            flash('Comment created successfully!', 'success')
        else:
            flash('Comment creation failed!', 'warning')

    items = Order.getOrderProduct(order_id)
    address = CustomerAddress.getByID(order.Order.address_id)
    customer = Customer.getByID(order.Customer.user_id)
    print(items)

    return render_template('order/orderDetails.html',
                            customer=customer,
                            address=address,
                            order=order,
                            items=items,
                            commentForm=commentForm
                        )



@login_required
def process(order_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    order = Order.getByID(order_id)
    order.Order.process()

    if order.Order.status == 'delivered':
        user = User.getByID(order.Order.customer_id)
        send_mail(recipients = [user.email],
                  subject    = '[Moonbird] Your order have been delivered.',
                  template   = 'mail/orderDelivered',
                  user       = user,
                  token      = user.create_order_token(order_id)
                 )

    return redirect(url_for('order.index', user_id=current_user.user_id))


def ex_comment(token):
    customer = Customer()
    data = customer.validate_confirm_token(token)

    if data is None:
        flash(f'You link is invalid or expired, please try again.', 'danger')
        return redirect(url_for('index.index'))

    customer = Customer.getByID(data.get('user_id'))
    customer.last_login = datetime.now()
    customer.update()
    login_user(customer)

    order_id = data.get('order_id')

    return redirect(url_for('order.details', order_id=order_id))
