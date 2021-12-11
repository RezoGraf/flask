from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length


class CreateUserForm(FlaskForm):
    username = StringField(label=('Username'),
                           validators=[DataRequired(),
                                       Length(max=64)])
    email = StringField(label=('Email'),
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)])
    password = PasswordField(label=('Password'),
                             validators=[DataRequired(),
                                         Length(min=8,
                                                message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
        label=('Confirm Password'),
        validators=[DataRequired(message='*Required'),
                    EqualTo('password',
                            message='Пароли должны быть одинаковыми!')])
    receive_emails = BooleanField(label=('Receive merketting emails.'))
    submit = SubmitField(label=('Submit'))


class UserRegistrationForm(FlaskForm):
    # ...
    submit = SubmitField(label=('Submit'))

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&amp;/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")


class WtfTemplate2(FlaskForm):
    submit = SubmitField(label=('Submit'))
