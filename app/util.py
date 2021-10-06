import click;

from flask import current_app;
from flask.cli import with_appcontext;
from flask_sqlalchemy import SQLAlchemy;
from flask_bootstrap import Bootstrap;
from flask_bcrypt import Bcrypt;
from flask_mail import Mail;
from flask_login import LoginManager;

db = SQLAlchemy(current_app);
bootstrap = Bootstrap(current_app);
bcrypt = Bcrypt(current_app);
mail = Mail(current_app);
login = LoginManager(current_app);
login.login_view = 'login'

from models import (
    # AdminType, Adminuser,
    User, UserAddress, UserPayment,
    ProductInventory, ProductCategory, Discount, Product
);

def init_db():
    db.drop_all();
    db.create_all();

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db();

    user = User.User(
            email      = 'user@domain.com',
            username   = 'user',
            password   = 'user',
            first_name = 'user',
            last_name  = 'user',
            admin_type = 'user',
            confirm    = True
        );

    admin = User.User(
            email      = 'admin@domain.com',
            username   = 'admin',
            password   = 'admin',
            first_name = 'admin',
            last_name  = 'admin',
            admin_type = 'admin',
            confirm    = True
        );

    staff = User.User(
            email      = 'staff@domain.com',
            username   = 'staff',
            password   = 'staff',
            first_name = 'staff',
            last_name  = 'staff',
            admin_type = 'staff',
            confirm    = True
        );

    category = ProductCategory.ProductCategory(
            name = 'category1',
            description = 'category1 description'
        );

    inventory = ProductInventory.ProductInventory(
            quantity = 100
        );

    product = Product.Product(
            inventory_id = inventory,
            category_id  = [category],
            name        = 'product',
            description = 'Product description',
            price       = 100
        );

    db.session.add_all([user, admin, staff]);
    db.session.commit();

    db.session.add(category);
    db.session.add(inventory);
    db.session.commit();
    db.session.add(product);
    db.session.commit();


    click.echo('Initialized the database.');

def init_app(app):
    app.cli.add_command(init_db_command);
