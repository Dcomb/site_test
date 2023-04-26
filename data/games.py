import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Games(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'games'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    game_name = sqlalchemy.Column(sqlalchemy.String)
    genre = sqlalchemy.Column(sqlalchemy.String)
    company = sqlalchemy.Column(sqlalchemy.String)
    size_GB = sqlalchemy.Column(sqlalchemy.Integer)
    version = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    multiplayer = sqlalchemy.Column(sqlalchemy.Boolean)
    description = sqlalchemy.Column(sqlalchemy.String)
    picture_url = sqlalchemy.Column(sqlalchemy.String)

