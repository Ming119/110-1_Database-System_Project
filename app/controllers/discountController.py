from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



@login_required
def index():
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    discounts = Discount.getAll()

    return render_template('manageDiscount.html', discounts=discounts)



@login_required
def create(type):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if type == 'shipping':
        createDiscountForm = CreateShippingDiscountForm()
    elif type == 'product':
        createDiscountForm = CreateproductDiscountForm()
    elif type == 'order':
        createDiscountForm = CreateOrderDiscountForm()

    if request.method == 'POST' and createDiscountForm.validate_on_submit():
        if type == 'shipping':
            if ShippingDiscount.create(
                discount_code = createDiscountForm.discount_code.data,
                name          = createDiscountForm.name.data,
                description   = createDiscountForm.description.data,
                start_at      = createDiscountForm.start_at.data,
                end_at        = createDiscountForm.end_at.data,
                atLeastAmount = createDiscountForm.atLeastAmount.data
            ):
                flash(f'Successfully created the shipping discount', 'success')

            else:
                flash(f'Error creating the shipping discount', 'warning')

        elif type == 'product':
            if ProductDiscount.create(
                discount_code      = createDiscountForm.discount_code.data,
                name               = createDiscountForm.name.data,
                description        = createDiscountForm.description.data,
                start_at           = createDiscountForm.start_at.data,
                end_at             = createDiscountForm.end_at.data,
                discountPercentage = createDiscountForm.discount_percentage.data
            ):
                flash(f'Successfully created the product discount', 'success')

            else:
                flash(f'Error creating the product discount', 'warning')

        elif type == 'order':
            if ProductDiscount.create(
                discount_code      = createDiscountForm.discount_code.data,
                name               = createDiscountForm.name.data,
                description        = createDiscountForm.description.data,
                start_at           = createDiscountForm.start_at.data,
                end_at             = createDiscountForm.end_at.data,
                discountPercentage = createDiscountForm.discount_percentage.data,
                atLeastAmount      = createDiscountForm.atLeastAmount.data
            ):
                flash(f'Successfully created the order discount', 'success')

            else:
                flash(f'Error creating the order discount', 'warning')

        return redirect(url_for('discount.index'))

    return render_template('createDiscount.html', createDiscountForm=createDiscountForm)



@login_required
def details(discount_code):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    discount = Discount.getByID(discount_code)

    return render_template('discountDetails.html', discount=discount)



@login_required
def update(discount_code):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    updateDiscountForm = UpdateDiscountForm()

    if request.method == 'POST' and updateDiscountForm.validate_on_submit():
        if Discount.update(
            name        = updateDiscountForm.name.data,
            description = updateDiscountForm.description.data,
            start_at    = updateDiscountForm.start_at.data,
            end_at      = updateDiscountForm.end_at.data
        ):
            flash(f'Successfully updated the discount', 'success')

        else:
            flash(f'Error updating the discount', 'warning')

    discount = Discount.getByID(discount_code)

    updateDiscountForm.name.data        = discount.name
    updateDiscountForm.description.data = discount.description
    updateDiscountForm.start_at.data    = discount.start_at
    updateDiscountForm.end_at.data      = discount.end_at

    return render_template('updateDetails.html', updateDiscountForm=updateDiscountForm)



@login_required
def delete(discount_code):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if Discount.delete(discount_code):
        flash(f'Successfully deleted the discount', 'success')

    else:
        flash(f'There was an error deleting the discount', 'warning')

    return redirect(url_for('discount.index'))
