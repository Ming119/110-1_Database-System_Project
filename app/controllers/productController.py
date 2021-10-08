from util import db;
from flask import flash, redirect, render_template, request, session, url_for;
from flask_login import login_user, current_user, login_required, logout_user;
from models import Product, ProductCategory;
from forms import Search, NewCategory, NewProduct;

def index():
    categories = ProductCategory.ProductCategory.query.all();

    form_search      = Search.Search();
    form_newCategory = NewCategory.NewCategory();
    form_newProduct  = NewProduct.NewProduct();
    form_newProduct.category.choices = [(category.category_id, category.name) for category in categories];

    # Create a new product
    if request.method == 'POST' and form_newProduct.validate_on_submit():
        return createProduct(form_newProduct);

    # Create a new category
    if request.method == 'POST' and form_newCategory.validate_on_submit():
        # if form_newCategory.validate_name(form_newCategory.name):
        return createCategory(form_newCategory);

    # Search
    if request.method == 'POST' and form_search.validate_on_submit():
        words = form_search.search.data.split(' ');

        products_list = list();

        for word in worlds:
            products_list.append(Product.Product.query.filter(Product.Product.name.contains(word)).all());
            products_list.append(Product.Product.query.filter(Product.Product.description.contains(word)).all());

        products = set(products_list);

    else:
        products = Product.Product.query.all();

    return render_template('product.html',
                            form_search      = form_search,
                            form_newCategory = form_newCategory,
                            form_newProduct  = form_newProduct,
                            categories       = categories,
                            products         = products
                        );

def details(product_id):
    pass;

def edit(product_id):
    pass;

def createProduct(form):
    product = Product.Product(
                inventory_id = 1,
                category_id  = form.category.data,
                name         = form.productName.data,
                description  = form.productDescription.data,
                price        = form.price.data
            );

    db.session.add(product);
    db.session.commit();

    return redirect(url_for('product.index'));

def createCategory(form):
    category = ProductCategory.ProductCategory(
                name        = form.categoryDame.data,
                description = form.categoryDescription.data
            );

    db.session.add(category);
    db.session.commit();

    flash(f'Category added successfully.', 'success');
    return redirect(url_for('product.index'));

def delete(product_id):
    pass;
