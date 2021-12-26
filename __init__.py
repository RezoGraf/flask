from api.api import api
from data_input.data_input import data_input
from excel.excel import excel
from report.report import report
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__, static_folder="static",
            template_folder='templates')
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.register_blueprint(data_input,
                       url_prefix='/data_input',
                       static_folder='/static',
                       template_folder='/templates')

app.register_blueprint(api, url_prefix='/api')

app.register_blueprint(excel, url_prefix='/excel')

app.register_blueprint(report, url_prefix='/report')


@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        if (username == 'root' and password == 'pass') or (username == 'kadr' and password == 'kadr') or (username == 'epid' and password == 'epid'): 
            return redirect(url_for('menu'))
        else:
            message = "Неверное имя пользователя или пароль"
    return render_template('login.html', message=message)


@app.route('/menu')
def menu():
    return render_template('menu.html')


if __name__ == "__main__":
    # app.run(host='192.168.100.142', port=80, debug=True)
    app.run('0.0.0.0')
