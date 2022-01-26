from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    DateField,
    SelectField,
    BooleanField
)
from wtforms.validators import (
    ValidationError,
    DataRequired,
    EqualTo,
    Length,
    URL
)

class WtfTemplate(FlaskForm):
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
    submit = SubmitField(label=('Выбрать'))


class WtfTemplate3(FlaskForm):
    submit = SubmitField(label=('Добавить'))

class WtfTemplate4(FlaskForm):
    submit = SubmitField(label=('Сохранить'))


class SignupForm(FlaskForm):
    """Sign up for a user account."""
    password = PasswordField(
        "Password",
        [DataRequired(message="Please enter a password.")],
    )
    confirmPassword = PasswordField(
        "Repeat Password",
        [EqualTo(password, message="Passwords must match.")]
    )
    title = SelectField(
        "Title",
        [DataRequired()],
        choices=[
            ("Farmer", "farmer"),
            ("Corrupt Politician", "politician"),
            ("No-nonsense City Cop", "cop"),
            ("Professional Rocket League Player", "rocket"),
            ("Lonely Guy At A Diner", "lonely"),
            ("Pokemon Trainer", "pokemon"),
        ],
    )
    website = StringField("Website", validators=[URL()])
    submit = SubmitField("Submit")
