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

    searchForm = SearchForm()

    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        discount_list = list()
        for word in words:
            discount_list.extend(Discount.query.filter(Discount.discount_code.contains(word)).all())
            discount_list.extend(Discount.query.filter(Discount.description.contains(word)).all())

        discounts = set(discount_list)

    else: discounts = Discount.getAll()

    discountCount = {'all': Discount.count(),
                     'product': Discount.countByType('product'),
                     'shipping': Discount.countByType('shipping'),
                     'order': Discount.countByType('order'),
                    }

    return render_template('manageDiscount.html',
                            searchForm    = searchForm,
                            discounts     = discounts,
                            discountCount = discountCount
                        )



@login_required
def filterIndex(type):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    searchForm = SearchForm()
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        discount_list = list()
        for word in words:
            discount_list.extend(Discount.query.filter(Discount.discount_code.contains(word), Discount.type==type).all())
            discount_list.extend(Discount.query.filter(Discount.description.contains(word), Discount.type==type).all())

        discounts = set(discount_list)

    else: discounts = Discount.getByType(type)

    discountCount = {'all': Discount.count(),
                     'product': Discount.countByType('product'),
                     'shipping': Discount.countByType('shipping'),
                     'order': Discount.countByType('order'),
                    }

    return render_template('manageDiscount.html',
                            searchForm    = searchForm,
                            discounts     = discounts,
                            discountCount = discountCount,
                            filter        = type
                        )



@login_required
def create(type):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if type == 'shipping':
        newDiscountForm = NewShippingDiscountForm()
    elif type == 'product':
        newDiscountForm = NewProductDiscountForm()
    elif type == 'order':
        newDiscountForm = NewOrderDiscountForm()

    if request.method == 'POST' and newDiscountForm.validate_on_submit():
        if newDiscountForm.code.data == '':
            flash(f'Code field is required', 'warning')
            return redirect(url_for('discount.create', type=type))

        if type == 'shipping':
            if ShippingDiscount.create(
                discount_code = newDiscountForm.code.data,
                description   = newDiscountForm.description.data,
                start_at      = newDiscountForm.start_at.data,
                end_at        = newDiscountForm.end_at.data,
                atLeastAmount = newDiscountForm.atLeastAmount.data
            ):
                flash(f'Successfully created the shipping discount', 'success')

            else:
                flash(f'Error creating the shipping discount', 'warning')

        elif type == 'product':
            if ProductDiscount.create(
                discount_code      = newDiscountForm.code.data,
                description        = newDiscountForm.description.data,
                start_at           = newDiscountForm.start_at.data,
                end_at             = newDiscountForm.end_at.data,
                discountPercentage = newDiscountForm.discountPercentage.data
            ):
                flash(f'Successfully created the product discount', 'success')

            else:
                flash(f'Error creating the product discount', 'warning')

        elif type == 'order':
            if OrderDiscount.create(
                discount_code      = newDiscountForm.code.data,
                description        = newDiscountForm.description.data,
                start_at           = newDiscountForm.start_at.data,
                end_at             = newDiscountForm.end_at.data,
                discountPercentage = newDiscountForm.discountPercentage.data,
                atLeastAmount      = newDiscountForm.atLeastAmount.data
            ):
                flash(f'Successfully created the order discount', 'success')

            else:
                flash(f'Error creating the order discount', 'warning')

        return redirect(url_for('discount.index'))

    return render_template('newDiscount.html', newDiscountForm=newDiscountForm)



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

    discount = Discount.getByCode(discount_code)
    if (discount.type == 'shipping'):
        updateDiscountForm = NewShippingDiscountForm()
    elif (discount.type == 'product'):
        updateDiscountForm = NewProductDiscountForm()
    elif (discount.type == 'order'):
        updateDiscountForm = NewOrderDiscountForm()

    if request.method == 'POST' and updateDiscountForm.validate_on_submit():
        if discount.update(
            description = updateDiscountForm.description.data,
            start_at    = updateDiscountForm.start_at.data,
            end_at      = updateDiscountForm.end_at.data
        ):
            flash(f'Successfully updated the discount', 'success')

        else:
            flash(f'Error updating the discount', 'warning')

    updateDiscountForm.initData(discount)

    return render_template('updateDiscount.html', updateDiscountForm=updateDiscountForm)



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
