from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email('Не правильно записан email')])
    pas = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100)])
    rememer = BooleanField('Запомнить', default=False)
    submint = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя: ')
    email = StringField('Email: ', validators=[Email('Некорретный email')])
    pas = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=4, max=100)])

    pas2 = PasswordField('Повтор пароль: ', validators=[DataRequired(), EqualTo('pas', message='Пароли не совпадают')])
    sub = SubmitField('Регистрация')