from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



@login_required
def index():
    form = dateBetweenForm.DateBetweenForm();

    data = None
    c = 0
    s = 0
    if request.method == 'POST' and form.validate_on_submit():
        data = Order.getAllByDate(form.fromDate.data, form.toDate.data)
        for d in data:
            c += 1
            s += d.Order.amount

    return render_template('report/index.html', form=form, data=data, c=c, s=s)
