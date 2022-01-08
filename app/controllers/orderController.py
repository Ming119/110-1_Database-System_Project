from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



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
                        'processing': Order.count(status=0),
                        'delivering': Order.count(status=1),
                        'delivered': Order.count(status=2),
                    }
    else:
        orderCount = {'all': Order.count(user_id),
                        'processing': Order.count(status=0, customer_id=user_id),
                        'delivering': Order.count(status=1, customer_id=user_id),
                        'delivered': Order.count(status=2, customer_id=user_id),
                    }

    return render_template('order/manageOrder.html',
                            searchForm = searchForm,
                            orders     = orders,
                            orderCount = orderCount,
                            filter     = -1
                        )


@login_required
def filterIndex(user_id, status):
    if current_user.role != 'staff':
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
                        'processing': Order.count(0),
                        'delivering': Order.count(1),
                        'delivered': Order.count(2),
                    }
    else:
        orderCount = {'all': Order.count(user_id),
                        'processing': Order.count(0, user_id),
                        'delivering': Order.count(1, user_id),
                        'delivered': Order.count(2, user_id),
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
    if current_user.role != 'staff' and current_user.user_id != order.customer_id:
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    orders = Order.getAll()
    form = NewProductForm(orders)

    form.initProductData(order)

    return render_template('order/orderDetail.html', form=form, orders=orders)
    #return render_template('order/manageOrder.html', order=order) #order/orderDeteail.html



@login_required
def update(order_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    order = Order.getByID(order_id)

    return render_template('order/manageOrder.html')    #FIXME
