from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class DownloadForm(FlaskForm):
    game_name = StringField('Название игры: ', validators=[DataRequired()])
    genre = StringField('Жанр: ', validators=[DataRequired()])
    size_GB = StringField('Размер в ГБ: ', validators=[DataRequired()])
    cost = StringField('Стоимость в рублях: ', validators=[DataRequired()])
    version = StringField('Версия: ', validators=[DataRequired()])
    multiplayer = SelectField('Наличие мультиплеера: ', validators=[DataRequired()], choices=[('Да'), ('Нет')])
    description = StringField('Краткое описание: ', validators=[DataRequired()])
    picture_url = StringField('URL аватара игры: ', validators=[DataRequired()])
    file = StringField('Приложите файл с сюжетом')
    submit = SubmitField('Зарегестрировать игру')
