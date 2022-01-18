from api.api import api
from data_input.data_input import data_input
from excel.excel import excel
from report.report import report
from db_test.db_test import db_test
import datetime
from flask import Flask, render_template, request, url_for, redirect, session
import auth
import errors
import logging


app = Flask(__name__, static_folder="static",
            template_folder='templates')
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'sdlfhwerfohw489fh48of4ho'
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.register_blueprint(data_input,
                       url_prefix='/data_input',
                       static_folder='/static',
                       template_folder='/templates')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(excel, url_prefix='/excel')
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(db_test, url_prefix='/db_test')


@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    message_auth = ""
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        auth_result = auth.check_credentials(username, password)
        if auth_result[0] == 'error':
            message_auth = auth_result[1]
        if auth_result[0] == 'ok':
            message_auth = f'AD: успешная авторизация {auth_result[1]}, доступ уровень {auth_result[2]}'
        if (username == 'root' and password == 'pass') or (auth_result[0] == 'ok'): 
            return redirect(url_for('menu'))
        else:
            message = "Неверное имя пользователя или пароль"
    return render_template('login.html', message=message, message_auth=message_auth)


@app.route('/menu')
def menu():
    if 'arena_user' in session:
        arena_user = session.get('arena_user')
    else:
        arena_user = 'none'
    if 'arena_fio' in session:
        arena_fio = session.get('arena_fio')
    else:
        arena_fio = "Не пользователь домена"
    if 'auth_group' in session:
        auth_group = session.get('auth_group')
    else:
        auth_group = 'none'
    return render_template('menu.html', arena_fio=arena_fio)


if __name__ == "__main__":
    # app.run(host='192.168.100.142', port=80, debug=True)
    app.run(host='0.0.0.0', port=7000)
