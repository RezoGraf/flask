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
    URL,
    InputRequired
)


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
    website = StringField("Website",
                          validators=[URL()])
    birthday = DateField("Your Birthday")
    submit = SubmitField("Submit")


class WtfTemplate(FlaskForm):

    submit = SubmitField(label=('Выбрать'))

class WtfTemplate2(FlaskForm):
    submit = SubmitField(label=('Выбрать'))

class WtfTemplate3(FlaskForm):
    # t = DateField('DatePicker', format='%Y-%m-%d')
    submit = SubmitField(label=('Добавить'))

