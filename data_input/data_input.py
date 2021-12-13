from flask import Blueprint, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
# регистрируем схему `Blueprint`
from data_input.models import SignupForm
from . import data_input

data_input = Blueprint('data_input', __name__)

# теперь в этой схеме, вместо экземпляра приложения
# 'app' используем экземпляр `Blueprint` с именем `data_input`.
# Связываем URL со схемой `data_input`


@data_input.route('/2')
def index():
    return "This is an example app"


# @data_input.route('/1', methods=['GET', 'POST'])
# def signup():
#     try:
#         """User sign-up form for account creation."""
#         form = models.SignupForm()
#         if form.validate_on_submit():
#             return redirect(url_for("success"))
#         return render_template(
#             "signup.jinja2",
#             form=form,
#             template="form-template",
#             title="Signup Form"
#         )
#     except TemplateNotFound:
#         abort(404)


@data_input.route('/', methods=['GET', 'POST'])
def signup():
    """User sign-up form for account creation."""
    form = SignupForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "signup.jinja2",
        form=form,
        template="form-template",
        title="Signup Form"
    )
