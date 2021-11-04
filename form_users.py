from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class TempLogin(FlaskForm):
    email = StringField('email: ', validators=[Email('!')])
    psw = PasswordField('пароль: ', validators=[DataRequired(), Length(min=6, max=200, message='!')])
    remember =  BooleanField('запомнить меня', default=False)
    submit = SubmitField('войти')

class Register(FlaskForm):
     name = StringField('имя: ', validators=[Length(min=3, max=70, message='!')])
     surname = StringField('фамилия: ', validators=[Length(min=3, max=70, message='!')])
     email = StringField('email: ', validators=[Email('!')])
     phone = StringField('мобильный номер', validators=[Length(min=4, max=11, message='!')])
     psw = PasswordField('пароль: ', validators=[DataRequired(), Length(min=6, max=200, message='!')])
     psw2 = PasswordField('повтор пароли: ', validators=[DataRequired(), EqualTo('psw', message='пароли не совпадают')])
     submit = SubmitField('регистрация')

class Test_form(FlaskForm):
    name = StringField('name: ', validators=[Length(min=3, max=70, message='не правильно заполнено поле')])
    email = StringField('email: ', validators=[Email('не правильно заполнено поле')])
    psw = PasswordField('password: ', validators=[DataRequired(), Length(min=8, max=255)])
    submit = SubmitField('submit')
