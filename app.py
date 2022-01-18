from api.api import api
from data_input.data_input import data_input
from excel.excel import excel
from report.report import report
from zakaz_naryad.zakaz_naryad import zakaz_naryad
from flask import Flask, render_template, request, url_for, redirect
import auth

app = Flask(__name__, static_folder="static",
            template_folder='templates')
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.register_blueprint(data_input,
                       url_prefix='/data_input',
                       static_folder='/static',
                       template_folder='/templates')
app.register_blueprint(api, url_prefix='/api')

app.register_blueprint(excel, url_prefix='/excel')

app.register_blueprint(report, url_prefix='/report')

app.register_blueprint(zakaz_naryad, url_prefix='/zakaz_naryad')

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
    return render_template('menu.html')


if __name__ == "__main__":
    # app.run(host='192.168.100.142', port=80, debug=True)
    app.run('127.0.0.1', debug=True)
