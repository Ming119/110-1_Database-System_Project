import os;
import pymysql;

from flask import Flask, render_template, url_for;

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
        import util;
        util.init_app(app);

    # Register Route Blueprint
    from routes import (
        indexRoute, userRoute, productRoute
    );
    app.register_blueprint(indexRoute.bp);
    app.register_blueprint(userRoute.bp);
    # app.register_blueprint(productRoute.bp);

    return app;
