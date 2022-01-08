'''
app/util.py
'''

from datetime import date
from flask import current_app
from flask.cli import with_appcontext
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
import click

mail      = Mail(current_app)
bcrypt    = Bcrypt(current_app)
bootstrap = Bootstrap(current_app)
db        = SQLAlchemy(current_app)
fa        = FontAwesome(current_app)
login     = LoginManager(current_app)
login.login_view = 'index.login'
login.login_message_category = 'danger'



from app.models import *
def init_db():
    '''
    Function to initialize the database
    Recreate the database
    '''

    db.drop_all()
    db.create_all()

@click.command('init-db')
@with_appcontext
def init_db_command():
    '''
    Function to initialize the database
    Initialize the data of the database

    Usage: flask init-db
    '''

    init_db()

    Admin.create(
            email      = 'admin@domain.com',
            username   = 'admin',
            password   = 'admin',
            first_name = 'admin',
            last_name  = 'admin',
        )

    Staff.create(
            email      = 'staff@domain.com',
            username   = 'staff',
            password   = 'staff',
            first_name = 'staff',
            last_name  = 'staff',
        )

    Customer.create(
            email      = 'customer@domain.com',
            username   = 'customer',
            password   = 'customer',
            first_name = 'customer',
            last_name  = 'customer',
            is_active  = True,
            DOB        = date.today()
        )

    ProductCategory.create(
            name = 'Shoes',
            description = 'Shoes'
        )

    ProductCategory.create(
            name = 'Watch',
            description = 'Watch'
        )

    Product.create(
            category_id = 1,
            quantity    = 1,
            name        = 'Shoe',
            description = 'Shoe description',
            price       = 100,
            image_url   = 'https://api.lorem.space/image/shoes?w=304&h=225'
        )

    Product.create(
            category_id = 2,
            quantity    = 1,
            name        = 'Watch',
            description = 'Watch description',
            price       = 100,
            image_url   = 'https://api.lorem.space/image/watch?w=304&h=225'
        )

    click.echo('Initialized the database.')

def init_app(currentApp):
    currentApp.cli.add_command(init_db_command)
