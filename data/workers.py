import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Workers(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'workers'


    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    worker_surname = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    worker_name = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    worker_age = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    company_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    registr_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_name = orm.relationship('User', foreign_keys=[worker_name])
    user_surname = orm.relationship('User', foreign_keys=[worker_surname])
    user_age = orm.relationship('User', foreign_keys=[worker_age])



