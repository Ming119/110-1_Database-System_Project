from util import db
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user, current_user, login_required, logout_user
from models import Product, ProductCategory
from forms import Search, NewCategory


def index():
    form_search = Search.Search()
    form_newCategory = NewCategory.NewCategory()

    if request.method == 'POST' and form_newCategory.validate_on_submit():
        return createCatedory(form_newCategory)

    if request.method == 'POST' and form_search.validate_on_submit():
        words = form.search.data.split(' ')

        products_list = [
            Product.Product.query.filter(Product.Product.name.contains(word)).all() 
            for word in words
        ]

        # for word in worlds:  # typo
        #     products_list.append(Product.Product.query.filter(
        #         Product.Product.name.contains(word)).all()
        #     )

        products = set(products_list)
    else:
        products = Product.Product.query.all()

    categories = ProductCategory.ProductCategory.query.all()

    return render_template(
        'product.html',
        form_search      = form_search,
        form_newCategory = form_newCategory,
        categories       = categories,
        products         = products
    )


def details(product_id):
    pass


def edit(product_id):
    pass


def createProduct(form_newProduct):
    pass


def createCatedory(form):
    category = ProductCategory.ProductCategory(
        name=form.name.data,
        description=form.description.data
    )

    db.session.add(category)
    db.session.commit()

    return redirect(url_for('product.index'))


def delete(product_id):
    pass
