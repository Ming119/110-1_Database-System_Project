import os;
import pymysql;

from flask import Flask, render_template, url_for;
from flask_bootstrap import Bootstrap;

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True);

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True);
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config);

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path);
    except OSError:
        pass;

    # Register the database with the Application
    with app.app_context():
        from . import db;
        db.init_app(app);

    bootstrap = Bootstrap(app);

    # Register Route Blueprint
    from routes import (
        index, user, product
    );
    app.register_blueprint(index.bp);
    app.register_blueprint(user.bp);
    # app.register_blueprint(product.bp);


    return app;