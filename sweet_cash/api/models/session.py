
from datetime import datetime
from flask_jwt_extended import create_access_token
from datetime import timedelta

from db import db
from api.models.base import BaseModel


class SessionModel(BaseModel):
    __tablename__ = 'sessions'
    updated_at = db.Column(db.DateTime, nullable=True)
    token = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    login_method = db.Column(db.String, nullable=True)
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, **kwargs):
        self.token = self.new_token()
        self.user_id = kwargs.get('user_id')
        self.login_method = kwargs.get('login_method')

    def new_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    def update(self, login_method: str):
        self.token = self.new_token()
        self.login_method = login_method
        self.updated_at = datetime.utcnow().isoformat()
        db.session.commit()

    @classmethod
    def get_user_id(cls, token: str):
        result = cls.query.filter(cls.token == token).first()
        if result is not None:
            return result.user_id
        return result

    @classmethod
    def get(cls, user_id=None, token=None):
        if user_id is not None:
            result = cls.query.filter(cls.user_id == user_id).first()
        elif token is not None:
            result = cls.query.filter(cls.token == token).first()
        else:
            result = None
        return result
