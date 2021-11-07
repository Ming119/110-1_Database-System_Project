import click

from flask import current_app, session, request, redirect, url_for, flash;
from flask.cli import with_appcontext;
from flask_sqlalchemy import SQLAlchemy;
from flask_bootstrap import Bootstrap;
from flask_bcrypt import Bcrypt;
from flask_mail import Mail;
from flask_login import LoginManager, current_user;
from functools import wraps
from datetime import datetime, date

db        = SQLAlchemy(current_app)
bootstrap = Bootstrap(current_app)
bcrypt    = Bcrypt(current_app)
mail      = Mail(current_app)
login     = LoginManager(current_app)
login.login_view = 'index.login'
login.login_message_category = 'danger'

from app.models import (
    User, CustomerAddress, CustomerPayment,
    ProductCategory, Product, #Discount
    ShoppingCart,
    Order
)

def init_db():
    db.drop_all()
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()

    User.Customer.create(
            email      = 'customer@domain.com',
            username   = 'customer',
            password   = 'customer',
            first_name = 'customer',
            last_name  = 'customer',
            DOB        = date.today()
        )

    User.Staff.create(
            email      = 'staff@domain.com',
            username   = 'staff',
            password   = 'staff',
            first_name = 'staff',
            last_name  = 'staff',
        )

    User.Admin.create(
            email      = 'admin@domain.com',
            username   = 'admin',
            password   = 'admin',
            first_name = 'admin',
            last_name  = 'admin',
        )

    ProductCategory.ProductCategory.create(
            name = 'category1',
            description = 'category1 description'
        )

    Product.Product.create(
            category_id = 1,
            quantity    = 1,
            name        = 'product',
            description = 'Product description',
            price       = 100
        )

    click.echo('Initialized the database.')

def init_app(current_app):
    current_app.cli.add_command(init_db_command)
