from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



@login_required
def index():
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    searchForm = SearchForm()
    order = Order.getAll()

    return render_template('order/manageOrder.html', order=order)

@login_required
def filterIndex(status):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    order = Order.getByStatus()

    return render_template('order/manageOrder.html',
                            order=order,
                            filter=status
                        )


@login_required
def details(order_id):

    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    order = Order.getByID(order_id)

    orders = Order.getAll()
    form = NewProductForm(orders)

    form.initProductData(order)
    return render_template('order/manageOrder.html', form=form, order=order)




    #return render_template('order/manageOrder.html', order=order) #order/orderDeteail.html



@login_required
def update(order_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    return render_template('order/manageOrder.html')    #FIXME
