__author__ = 'franksziebert@gmail.com'

"""
Many thanks to Bob Waycott and Miguel Grinberg for excellent code examples and advice:
https://bobwaycott.com/blog/how-i-use-flask/organizing-flask-models-with-automatic-discovery/
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
"""


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_utils import force_auto_coercion


from project.setup.loggers import LOGGERS
from project.lib.loaders import load_models

__all__ = ('db', 'init_db')

log = LOGGERS.Setup
# our global DB object (imported by models & views & everything else)
db = SQLAlchemy()
# support importing a functioning session query
query = db.session.query
# our global migrate object
migrate = Migrate()


def init_db(app=None, db=None):
    """
    Initializes the global database object used by the app.

    Code base courtesy of:
    https://bobwaycott.com/blog/how-i-use-flask/organizing-flask-models-with-automatic-discovery/

    """
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        force_auto_coercion()
        load_models()
        database_url = app.config['SETUP'].DATABASE_URL
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        # migrate.init_app(app, db)
        log.info(f'Database Successfully configured.')
    else:
        raise ValueError('Cannot init DB without db and app objects.')


