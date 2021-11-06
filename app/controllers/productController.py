from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, current_user, login_required, logout_user
from app.models import Product, ProductCategory
from app.forms import Search, NewCategory, NewProduct

# PMS page of the website
# GET method to render PMS page
# POST method for create category, create product or search function
def index():
    categories = ProductCategory.ProductCategory.query.all()

    form_search      = Search.Search()
    form_newCategory = NewCategory.NewCategory()
    form_newProduct  = NewProduct.NewProduct()
    form_newProduct.category.choices = [(category.category_id, category.name) for category in categories]

    # Create a new category
    if request.method == 'POST' and form_newCategory.validate_on_submit():
        return createCategory(form_newCategory)

    # Create a new product
    if request.method == 'POST' and form_newProduct.validate_on_submit():
        return createProduct(form_newProduct)

    # Search
    if request.method == 'POST' and form_search.validate_on_submit():
        words = form_search.search.data.split(' ')

        products_list = list()
        for word in words:
            products_list.append(p for p in Product.Product.query.filter(Product.Product.name.contains(word)).all())
            products_list.append(p for p in Product.Product.query.filter(Product.Product.description.contains(word)).all())

        products = set(products_list)

    else:
        products = Product.Product.query.all()

    return render_template('manageProduct.html',
                            form_search      = form_search,
                            form_newCategory = form_newCategory,
                            form_newProduct  = form_newProduct,
                            categories       = categories,
                            products         = products
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

    elif ProductCategory.ProductCategory.query.filter_by(name=form.categoryName.data).first() is not None:
        flash(f'Category already exists.', 'warning')

    else:
        ProductCategory.create(name        = form.categoryName.data,
                               description = form.categoryDescription.data
                              )
        flash(f'Category added successfully.', 'success')

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

    elif Product.Product.query.filter_by(name=form.productName.data).first() is not None:
        flash(f'Product already exists.', 'warning')

    else:
        Product.create(category_id = form.category.data,
                       name        = form.productName.data,
                       description = form.productDescription.data,
                       price       = form.price.data,
                       quantity    = form.quantity.data
                      )

        flash(f'Product created successfully', 'success')

    return redirect(url_for('product.index'))

def details(product_id):
    product = Product.Product.query.filter_by(product_id=product_id).first()
    categories = ProductCategory.ProductCategory.query.all()
    form = NewProduct.NewProduct(
                productName        = product.name,
                productDescription = product.description,
                price              = product.price,
                quantity           = product.quantity,
                category           = product.category_id
            )
    form.category.choices = [(category.category_id, category.name) for category in categories]

    # Edit
    if request.method == 'POST' and form.validate_on_submit():
        return edit(product, form)

    return render_template('productDetails.html', form=form, product=product)

@login_required
def edit(product, form):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    elif form.productName.data != product.name and Product.Product.query.filter_by(name=form.productName.data).first() is not None:
        flash(f'Product already exists.', 'warning')

    else:
        product.name        = form.productName.data
        product.description = form.productDescription.data
        product.category_id = form.category.data
        product.price       = form.price.data
        product.quantity    = form.quantity.data

        product.update()

        flash(f'Product updated successfully.', 'success')

    return redirect(url_for('product.details', product_id=product.product_id))

# delete category funciton
# :param: category_id
#   delete category based on category_id
# redirect to PMS page and flash message after category is deleted
@login_required
def deleteCategory(category_id):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    else:
        try:
            ProductCategory.ProductCategory.query.filter_by(category_id=category_id).delete()

        except:
            flash(f'This Category is still in use.', 'warning')

        else:
            ProductCategory.delete()
            flash(f'Category deleted successfully.', 'success')

    return redirect(url_for('product.index'))

# delete product funciton
# :param: product_id
#   delete product based on category_id
# redirect to PMS page and flash message after product is deleted
@login_required
def deleteCategory(category_id):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')

    else:
        try:
            ProductCategory.ProductCategory.query.filter_by(category_id=category_id).delete()
        except:
            flash(f'This Category is still in use.', 'warning')
        else:
            db.session.commit()
            flash(f'Category deleted successfully.', 'success')

    return redirect(url_for('product.index'))

@login_required
def deleteProduct(product_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
    else:
        Product.Product.query.filter_by(product_id=product_id).delete()
        Product.delete()

        flash(f'Product deleted successfully.', 'success')

    return redirect(url_for('product.index'))
