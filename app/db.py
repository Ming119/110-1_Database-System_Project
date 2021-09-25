import click;

from flask import current_app;
from flask.cli import with_appcontext;
from flask_sqlalchemy import SQLAlchemy;

db = SQLAlchemy(current_app);

from models import User, Product;

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
