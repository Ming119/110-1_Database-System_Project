from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



@login_required
def index():
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    return render_template('order/manageOrder.html')



@login_required
def details(order_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    return render_template('order/orderDetails.html')



@login_required
def update(order_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    return render_template('order/manageOrder.html')    #FIXME
