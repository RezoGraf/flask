from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField

class RegistrationForm(Form):
    username = StringField('Имя пользователя', [validators.Length(min=4, max=25)])
    email = StringField('Email-адрес', [validators.Length(min=6, max=35)])
    password = PasswordField('Новый пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])
    confirm = PasswordField('Повторите пароль')
    accept_tos = BooleanField('Я принимаю TOS', [validators.DataRequired()])
    select = SelectField('Pick Name', choices=choices)
    