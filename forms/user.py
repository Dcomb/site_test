from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    nickname = StringField('Позывной:')
    name = StringField('Имя:')
    age = StringField('Возраст:')
    games = StringField('Игры приобретенны:')
    position = StringField('Роль на сайте:')
    new_url = StringField('', validators=[DataRequired()])
    submit = SubmitField('Изменить аватар')