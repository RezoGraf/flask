from flask import Blueprint, render_template, request, redirect, url_for
# from flask_wtf import FlaskForm
from app.menu_script import generate_menu
# from app.epid.models import RegistrationForm
from webargs import flaskparser, fields

epid = Blueprint('epid', __name__)



@epid.route('/<podr>/<otd>')
def epid_workers(podr = 0, otd = 0):
    menu = generate_menu()
    print(f'podr= {podr}, otd= {otd}')
    return render_template('epid_workers.html', menu=menu)

@epid.route('/')
def main():
    menu = generate_menu()
    # print(f'podr= {podr}, otd= {otd}')
    # создаем экземпляр класса формы

    # если HTTP-метод POST и данные формы валидны
    if request.method == 'POST':
        # используя схему `SQLAlchemy` создаем объект, 
        # для последующей записи в базу данных
        FORM_ARGS = {
            'email': fields.Email(required=True),
            'username': fields.Str(required=True),
            'select_otd': fields.Str(required=True)}
        parsed_args = flaskparser.parser.parse(FORM_ARGS, request)
        return redirect(url_for('login'))
    return render_template('epid_workers.html', menu=menu)
