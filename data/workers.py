import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class Workers(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'workers'


    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    worker_surname = sqlalchemy.Column(sqlalchemy.String)
    worker_name = sqlalchemy.Column(sqlalchemy.String)
    worker_age = sqlalchemy.Column(sqlalchemy.Integer)
    company_name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    registr_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    orm_user = orm.relationship('User')




