"""
Many thanks to Bob Waycott on providing a clean structure to build upon.

Code derived largely from example provided by:
https://bobwaycott.com/blog/how-i-use-flask/query-helpers-for-sqlalchemy-models/

"""


###########################################
# Library import statements
###########################################


from arrow import utcnow
from sqlalchemy.ext.declarative import declared_attr, has_inherited_table
from sqlalchemy_utils import ArrowType
from sqlalchemy.exc import StatementError


###########################################
# Project import statements
###########################################


from project.db import db
from project.setup.loggers import LOGGERS
from .mixins.query import QueryMixin


log = LOGGERS.Database


__all__ = ('Model', 'ApiDatabaseError', )


class ApiDatabaseError(Exception):
    """
    AuthError Exception
        A standardized way to communicate auth failure modes
    """
    def __init__(self, status_code, message):
        self.message = message
        self.status_code = status_code


class Model(db.Model, QueryMixin):
    """Abstract base class for all app models.

    Provides an `id` & `created_at` column to every model.

    To define models, follow this example:

        from .base import Model

        class MyModel(Model):
            # model definition
    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def created_at(cls):
        return db.Column(ArrowType, default=utcnow, nullable=False, index=True)

    @property
    def class_name(self):
        """Shortcut for returning class name."""
        return unicode(self.__class__.__name__)

    @classmethod
    def __ignore__(cls):
        """Custom class attr that lets us control which models get ignored.

        We are using this because knowing whether or not we're actually dealing
        with an abstract base class is only possible late in the class's init
        lifecycle.

        This is used by the dynamic model loader to know if it should ignore.
        """
        return cls.__name__ in ('Model',)  # can add more abstract base classes here

    def __repr__(self):
        """"Returns a string representation of every object.

        Useful for logging & error reporting.
        Example:

            >>> obj = MyModel()
            >>> print obj
            MyModel.123

        Can be overridden by subclasses to customize string representation.
        """
        return u"{}.{}".format(self.class_name, self.id)

    @declared_attr
    def __tablename__(cls):
        """Generate a __tablename__ attr for every model that does not have
        inherited tables.

        Ensures table names match the model name without needing to declare it.
        """
        if has_inherited_table(cls):
            return None
        return cls.__name__.lower()

    ##################################################################################
    # I added the base methods below to augment the foundation built up by bob waycott
    ##################################################################################

    @property
    def dictionary(self):
        return {}

    @property
    def __skip_attrs__(self):
        return []

    def update(self, data):
        caught_id = data.get('id')
        if caught_id and self.id != caught_id:
            _id = self.id
            db.session.close()
            raise ApiDatabaseError(403,
                                   f"Cannot modify primary keys got:({caught_id}) for: {_id}")
        invalid_keys = list()
        for key, value in data.items():
            if any([key == skip for skip in self.__skip_attrs__]) or not hasattr(self, key):
                invalid_keys.append(value)
        if len(invalid_keys) > 0:
            db.session.close()
            raise ApiDatabaseError(422, f"Invalid Database Fields: {','.join(invalid_keys)}")
        else:
            for key, value in data.items():
                try:
                    setattr(self, key, value)
                except Exception as e:
                    log.exception(e)
                    db.session.close()
                    raise ApiDatabaseError(400, f"Rejected for : {key}")
            try:
                returns = self.dictionary
                self.save()
                db.session.close()
                return returns
            except StatementError as e:
                db.session.close()
                raise ApiDatabaseError(400, f'Rejected for: {e.orig}')
        raise ApiDatabaseError(400, f'Rejected!')

    @staticmethod
    def toTimeString(time_stamp):
        timezone = 'US/Mountain'
        return str(time_stamp.to(timezone))
