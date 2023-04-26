from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GameForm(FlaskForm):
    text = StringField('Введите название игры:', validators=[DataRequired()])
    submit = SubmitField('Поиск')
    game_name = StringField('название', validators=[DataRequired()])

