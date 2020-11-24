from flask_login import UserMixin
from .base import Model
from project.db import db
from project.setup.loggers import LOGGERS
from sqlalchemy_utils import ArrowType
from arrow import utcnow

__all__ = ('UserProfile', )


log = LOGGERS.Database


class UserProfile(UserMixin, Model):
    """
    .base.Model provides:
        id (primary key)
        created_at (creation date)
    flask_login.UserMixin provides:
    """

    alternate_id = db.Column(db.String(256), nullable=False, unique=True)
    social_id = db.Column(db.String(256), nullable=True, unique=True)
    nickname = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(256), nullable=True)
    picture = db.Column(db.String(256), nullable=True)
    name = db.Column(db.String(256), nullable=True)
    family_name = db.Column(db.String(256), nullable=True)
    given_name = db.Column(db.String(256), nullable=True)
    locale = db.Column(db.String(16), default='en', nullable=False)
    updated_at = db.Column(ArrowType, default=utcnow, index=True)
    email_verified = db.Column(db.Boolean, nullable=True, default=False)

    def __repr__(self):
        return f'<User {self.id}: email: {self.email} nickname: {self.nickname}>'

    @property
    def __skip_attrs__(self):
        return [
            "__repr__", 'records', 'manager', 'patron', 'provider', 'scheduler', 'addresses', 'created_at','update'
        ]

    @property
    def dictionary(self):
        return {
            'id': self.id,
            'created_at': self.toTimeString(self.created_at),
            'alternate_id': self.alternate_id,
            'social_id': self.social_id,
            'email': self.email,
            'email_verified': self.email_verified,
            'name': self.name,
            'family_name': self.family_name,
            'given_name': self.given_name,
            'locale': self.locale,
            'updated_at': self.toTimeString(self.updated_at),
        }

    @property
    def all_records(self):
        return []

    @property
    def all_records_serialized(self):
        return []

    @classmethod
    def get_or_create(cls, sub):
        existing_user = cls.query.filter(cls.alternate_id == sub).one_or_none()
        if existing_user:
            return existing_user
        else:
            new_user = cls(alternate_id=sub)
            new_user.save()
            this_id = new_user.id
            db.session.close()
            initialized_user = cls.get(this_id)
            return initialized_user
