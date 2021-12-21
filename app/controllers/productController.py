from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



# PMS page of the website
# GET method to render PMS page
# POST method for create category, create product or search function
def index():
    categories = ProductCategory.getAll()

    searchForm      = SearchForm()
    newCategoryForm = NewCategoryForm()
    newProductForm  = NewProductForm(categories)

    # Create a new category
    if request.method == 'POST' and newCategoryForm.validate_on_submit():
        return createCategory(newCategoryForm)

    # Create a new product
    if request.method == 'POST' and newProductForm.validate_on_submit():
        return createProduct(newProductForm)

    # Search
    if request.method == 'POST' and searchForm.validate_on_submit():
        words = searchForm.search.data.split(' ')

        products_list = list()
        for word in words:
            products_list.extend(Product.query.filter(Product.name.contains(word)).all())
            products_list.extend(Product.query.filter(Product.description.contains(word)).all())

        products = set(products_list)

    else:
        products = Product.getAll()

    return render_template('manageProduct.html',
                            searchForm      = searchForm,
                            newCategoryForm = newCategoryForm,
                            newProductForm  = newProductForm,
                            categories      = categories,
                            products        = products
                        )



# create category function
# :param: form
#   create category based on a validate form
# redirect to PMS page and flash a message after the category is created
@login_required
def createCategory(form):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    elif ProductCategory.create(name        = form.categoryName.data,
                                description = form.categoryDescription.data
                               ):
        flash(f'Category added successfully.', 'success')

    else:
        flash(f'Category already exists.', 'warning')

    return redirect(url_for('product.index'))



# create prodcut function
# :param: form
#   create product based on a validate form
# redirect to PMS page and flash message after the product is created
@login_required
def createProduct(form):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    elif Product.create(category_id = form.category.data,
                   name        = form.productName.data,
                   description = form.productDescription.data,
                   price       = form.price.data,
                   quantity    = form.quantity.data,
                   image_url   = form.image_url.data
                  ):
        flash(f'Product created successfully', 'success')

    else:
        flash(f'Product already exists.', 'warning')

    return redirect(url_for('product.index'))



def details(product_id):
    product = Product.getByID(product_id);

    if current_user.is_authenticated and current_user.role == 'staff':
        categories = ProductCategory.getAll()
        form = NewProductForm(
                    productName        = product.name,
                    productDescription = product.description,
                    price              = product.price,
                    quantity           = product.quantity,
                    category           = product.category_id,
                    categories = categories
                )
        # Edit
        if request.method == 'POST' and form.validate_on_submit():
            return edit(product, form)

        return render_template('productDetails.html', form=form, product=product)

    else:
        category = ProductCategory.getByID(product.category_id)

        form = AddToCardForm()

        # Add To Card
        if request.method == 'POST' and form.validate_on_submit():
            return addToCard(form)

        return render_template('productDetails.html', form=form, product=product, category=category)



@login_required
def edit(product, form):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    elif form.productName.data != product.name and Product.getByProductName(form.productName.data) is not None:
        flash(f'Product already exists.', 'warning')

    else:
        product.update(name        = form.productName.data,
                       description = form.productDescription.data,
                       category_id = form.category.data,
                       price       = form.price.data,
                       quantity    = form.quantity.data
                      )

        flash(f'Product updated successfully.', 'success')

    return redirect(url_for('product.details', product_id=product.product_id))



# @login_required
# def addToCard(form):



# delete category funciton
# :param: category_id
#   delete category based on category_id
# redirect to PMS page and flash message after category is deleted
@login_required
def deleteCategory(category_id):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    elif ProductCategory.deleteByID(category_id):
        flash(f'Category deleted successfully.', 'success')

    else:
        flash(f'Category is still in use.', 'warning')

    return redirect(url_for('product.index'))



# delete product funciton
# :param: product_id
#   delete product based on category_id
# redirect to PMS page and flash message after product is deleted
@login_required
def deleteProduct(product_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    elif Product.deleteByID(product_id):
        flash(f'Product deleted successfully.', 'success')

    else:
        flash(f'Product deleted failed.', 'warning')

    return redirect(url_for('product.index'))
