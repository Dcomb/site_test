from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CartaForm(FlaskForm):
    numb = StringField('Номер карты', validators=[DataRequired()])
    name_surname = StringField('Имя, фамилия владельца', validators=[DataRequired()])
    month = StringField('Срок действия  (Месяц', validators=[DataRequired()])
    year = StringField('Год)', validators=[DataRequired()])
    cvv = StringField('cvv', validators=[DataRequired()])
    submit = SubmitField('Оплатить')