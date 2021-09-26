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
    AdminType, Adminuser, User, UserAddress, UserPayment,
    Discount, Product, ProductCategory, ProductInventory
);

def init_db():
    db.drop_all();
    db.create_all();

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db();
    click.echo('Initialized the database.');

def init_app(app):
    app.cli.add_command(init_db_command);
