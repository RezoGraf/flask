from flask import Blueprint, render_template, request, redirect, url_for, session
from app.menu_script import generate_menu
from webargs import fields, validate
from webargs.flaskparser import use_args
from . import vaccine


vaccine = Blueprint('vaccine', __name__)



# @use_args({"name": fields.Str(validate=[validate.Range(min=1, max=999)],required=True)}, location="query")


@vaccine.route('/')
@use_args({"name": fields.Str(required=True, validate=[validate.Length(min=3, max=9999)])}, location="query")
def main(args):
    if 'arena_mpp' not in session:
        return redirect(url_for("login"))
    else:
        menu = generate_menu()
        name = args['name']
        # print(f'podr= {podr}, otd= {otd}')
        # создаем экземпляр класса формы

        # если HTTP-метод POST и данные формы валидны
        if request.method == 'POST':
            # используя схему `SQLAlchemy` создаем объект, 
            # для последующей записи в базу данных
            # FORM_ARGS = {
            #     'email': fields.Email(required=True),
            #     'username': fields.Str(required=True),
            #     'select_otd': fields.Str(required=True)}
            return redirect(url_for('login'))
        return render_template('vaccine_workers.html', menu=menu, name=name)
