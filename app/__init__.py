'''
app/__init__.py
'''

import os
from flask import Flask

def create_app(test_config=None):
    '''
    Entry function to the entire application
    '''

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the database with the Application
    with app.app_context():
        from app.util import init_app   # pylint: disable=import-outside-toplevel
        init_app(app)

    from app.routes import (
        indexRoute, userRoute, productRoute, discountRoute, orderRoute, report_route
    )    # pylint: disable=import-outside-toplevel
    # Register Route Blueprint
    app.register_blueprint(indexRoute.bp)
    app.register_blueprint(userRoute.bp)
    app.register_blueprint(productRoute.bp)
    app.register_blueprint(discountRoute.bp)
    app.register_blueprint(orderRoute.bp)
    app.register_blueprint(report_route.bp)

    return app
