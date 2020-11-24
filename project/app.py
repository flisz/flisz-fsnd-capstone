"""
Many thanks to Bob Waycott and Miguel Grinberg for excellent code examples and advice:
https://bobwaycott.com/blog/how-i-use-flask/organizing-flask-models-with-automatic-discovery/
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
"""

from copy import deepcopy
from flask import Flask
from flask_cors import CORS
from flask_wtf import CSRFProtect
from flask_login import LoginManager


from project.setup import SetupConfig
from project.setup.loggers import LOGGERS
from project.db import db, init_db

from project.auth import login_manager
from project.routes import init_routes


csrf = CSRFProtect()


def create_app(config_yaml=None):
    """Default application factory.

    Default usage:
        app = create_app()

    Usage with config file:
        app = create_app('/path/to/config.yml')

    If config_file is not provided, will look for default
    config expected at '<proj_root>/config/config.yml'.
    Returns Flask app object.
    Raises EnvironmentError if config_file cannot be found.
    """

    setup = SetupConfig(config_yaml=config_yaml)

    # start app setup
    app = Flask(__name__, template_folder=setup.TEMPLATES, static_folder=setup.STATIC_FILES)
    CORS(app)
    app.config['SETUP'] = deepcopy(setup)
    app.config['SECRET_KEY'] = deepcopy(setup.SECRET_KEY)

    set_app_mode(app)
    login_manager.init_app(app)
    # setup csrf
    if not app.testing:
        csrf.init_app(app)

    # setup db
    init_db(app, db)

    # todo: remove these two lines and replace with migrate
    #db.drop_all()
    #db.create_all()

    # register routes
    init_routes(app)

    return app


def set_app_mode(app):
    # set some helpful attrs to greatly simplify state checks
    setup = app.config['SETUP']
    app.env = setup.APP_MODE
    if app.env == 'test':
        # app.config['SERVER_NAME'] = f"{deepcopy(app.config['SETUP'].PROJECT_NAME)}.dev"
        app.testing = True
        app.debug = True
        app.live = False
    elif app.debug:
        app.live = False
        if app.env == 'development':
            app.dev = True
    elif app.env == 'development':  # but debug is off
        app.live = False
        app.testing = False
    elif app.env == 'production':
        app.live = True
    else:
        raise EnvironmentError('Invalid environment for app state.')


