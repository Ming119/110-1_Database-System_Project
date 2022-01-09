from app.models import *
from app.forms import *
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required



# PMS page of the website
# GET method to render PMS page
# POST method for create category, create product or search function
@login_required
def index():
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    categories = ProductCategory.getAll()
    discounts  = Discount.getByType('product')

    searchForm      = SearchForm()
    newCategoryForm = NewCategoryForm()
    newProductForm  = NewProductForm(ProductCategory.dropInactive(categories), discounts)

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
            products_list.extend(Product.getAllJoinedProductContains(word))

        products = set(products_list)

    else: products = Product.getAllJoinedProduct()

    categoryCount = {category.category_id: Product.countProductByCategory(category.category_id) for category in categories}
    categoryCount[0] = Product.count()

    return render_template('product/manageProduct.html',
                            searchForm      = searchForm,
                            newCategoryForm = newCategoryForm,
                            newProductForm  = newProductForm,
                            categories      = categories,
                            categoryCount   = categoryCount,
                            products        = products
                        )



@login_required
def filterIndex(category_id):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    categories = ProductCategory.getAll()
    discounts  = Discount.getByType('product')

    searchForm      = SearchForm()
    newCategoryForm = NewCategoryForm()
    newProductForm  = NewProductForm(categories, discounts)

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
            products_list.extend(Product.getAllJoinedProductByCategoryIDContains(category_id, word))
            products_list.extend(Product.getAllJoinedProductByCategoryIDContains(category_id, word))

        products = set(products_list)

    else: products = Product.getAllJoinedProductByCategoryID(category_id)

    categoryCount = {category.category_id: Product.countProductByCategory(category.category_id) for category in categories}
    categoryCount[0] = Product.count()

    return render_template('product/manageProduct.html',
                            searchForm      = searchForm,
                            newCategoryForm = newCategoryForm,
                            newProductForm  = newProductForm,
                            categories      = categories,
                            categoryCount   = categoryCount,
                            products        = products,
                            filter          = category_id
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
        return redirect(url_for('index.index'))

    if Product.create(category_id = form.category.data,
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
        discounts  = Discount.getByType('product')
        form = NewProductForm(categories, discounts)
        # Edit
        if request.method == 'POST' and form.validate_on_submit():
            return edit(product, form)

        form.init(product)
        return render_template('product/productDetails.html', form=form, product=product)

    else:
        if not product.is_active:
            flash(f'You are not allowed to access.', 'danger')
            return redirect(url_for('index.index'))

        category = ProductCategory.getByID(product.category_id)
        discount = ProductDiscount.getByCode(product.discount_code)
        form = AddToCartForm()

        # Add To Card
        if request.method == 'POST' and form.validate_on_submit():
            return addToCart(form, product, discount)

        return render_template('product/productDetails.html', form=form, product=product, category=category, discount=discount)



@login_required
def edit(product, form):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if form.productName.data != product.name and Product.getByProductName(form.productName.data) is not None:
        flash(f'Product already exists.', 'warning')

    else:
        if form.discount.data == 'None':
            dc = None
        else:
            dc = form.discount.data

        product.update(name         = form.productName.data,
                       description  = form.productDescription.data,
                       category_id  = form.category.data,
                       discount_code = dc,
                       price        = form.price.data,
                       quantity     = form.quantity.data
                      )

        flash(f'Product updated successfully.', 'success')

    return redirect(url_for('product.details', product_id=product.product_id))



@login_required
def addToCart(form, product, discount):
    item = CartItem.query.filter_by(cart_id=current_user.user_id, product_id=product.product_id).first()
    quantity   = form.quantity.data
    amount     = product.price * quantity

    if item is None:
        if (CartItem.create(
            cart_id    = current_user.user_id,
            product_id = product.product_id,
            quantity   = quantity,
            amount     = amount
        )):
            flash(f'Added to cart successfully', 'success')

        else:
            flash(f'Failed to add to cart', 'warning')

    else:
        if (item.update(item.quantity+quantity, item.amount+amount)):
            flash(f'Added to cart successfully', 'success')

        else:
            flash(f'Failed to add to cart', 'warning')

    return redirect(url_for('product.details', product_id=product.product_id))



# delete category funciton
# :param: category_id
#   delete category based on category_id
# redirect to PMS page and flash message after category is deleted
@login_required
def withholdCategory(category_id):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if ProductCategory.withholdByID(category_id):
        flash(f'Category withhold successfully.', 'success')

    else:
        flash(f'Category is still in use.', 'warning')

    return redirect(url_for('product.index'))



@login_required
def publishCategory(category_id):
    # access control
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if ProductCategory.publishByID(category_id):
        flash(f'Category publish successfully.', 'success')

    else:
        flash(f'Category publish failed.', 'warning')

    return redirect(url_for('product.index'))



# delete product funciton
# :param: product_id
#   delete product based on category_id
# redirect to PMS page and flash message after product is deleted
@login_required
def withholdProduct(product_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if Product.withholdByID(product_id):
        flash(f'Product withhold successfully.', 'success')

    else:
        flash(f'Product withhold failed.', 'warning')

    return redirect(url_for('product.index'))



@login_required
def publishProduct(product_id):
    if current_user.role != 'staff':
        flash(f'You are not allowed to access.', 'danger')
        return redirect(url_for('index.index'))

    if Product.publishByID(product_id):
        flash(f'Product publish successfully.', 'success')

    else:
        flash(f'Product publish failed.', 'warning')

    return redirect(url_for('product.index'))
