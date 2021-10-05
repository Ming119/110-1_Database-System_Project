from util import db;
from flask import flash, redirect, render_template, request, session, url_for;
from flask_login import login_user, current_user, login_required, logout_user;
from models import Product, ProductCategory;
from forms import Search;

def index():
    form = Search.Search();

    if request.method == 'POST' and form.validate_on_submit():
        words = form.search.data.split(' ');

        products_list = list();

        for word in worlds:
            products_list.append(Product.Product.query.filter(Product.Product.name.contains(word)).all());

        products = set(products_list);

    else:
        products = Product.Product.query.all();

    categories = ProductCategory.ProductCategory.query.all();

    return render_template('product.html', form=form, categories=categories, products=products);

def search(str):

    return render_template('product.html', category=category, products=products);

def details(product_id):
    pass;

def edit(product_id):
    pass;

def create():
    pass;

def delete(product_id):
    pass;
