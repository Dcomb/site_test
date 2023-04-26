from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    nickname = StringField('Позывной пользователя', validators=[DataRequired()])
    age = StringField('Возраст пользователя', validators=[DataRequired()])
    position = SelectField('Кем являетесь', validators=[DataRequired()], choices=[('Простой пользователь'), ('Разработчик')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')