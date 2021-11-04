import click

from flask import current_app, session, request, redirect, url_for, flash;
from flask.cli import with_appcontext;
from flask_sqlalchemy import SQLAlchemy;
from flask_bootstrap import Bootstrap;
from flask_bcrypt import Bcrypt;
from flask_mail import Mail;
from flask_login import LoginManager, current_user;
from functools import wraps

db        = SQLAlchemy(current_app)
bootstrap = Bootstrap(current_app)
bcrypt    = Bcrypt(current_app)
mail      = Mail(current_app)
login     = LoginManager(current_app)
login.login_view = 'index.login'
login.login_message_category = 'danger'

from app.models import (
    User, UserAddress, UserPayment,
    ProductCategory, Discount, Product
)

def init_db():
    db.drop_all()
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()

    user = User.User(
            email      = 'user@domain.com',
            username   = 'user',
            password   = 'user',
            first_name = 'user',
            last_name  = 'user',
            role       = 'user',
            confirm    = True
        )

    admin = User.User(
            email      = 'admin@domain.com',
            username   = 'admin',
            password   = 'admin',
            first_name = 'admin',
            last_name  = 'admin',
            role       = 'admin',
            confirm    = True
        )

    staff = User.User(
            email      = 'staff@domain.com',
            username   = 'staff',
            password   = 'staff',
            first_name = 'staff',
            last_name  = 'staff',
            role       = 'staff',
            confirm    = True
        )

    category = ProductCategory.ProductCategory(
            name = 'category1',
            description = 'category1 description'
        )

    product = Product.Product(
            category_id = 1,
            quantity    = 1,
            name        = 'product',
            description = 'Product description',
            price       = 100
        )

    user.create()
    admin.create()
    staff.create()
    category.create()
    product.create()

    click.echo('Initialized the database.')

def init_app(current_app):
    current_app.cli.add_command(init_db_command)
