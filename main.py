from flask import Flask, render_template, request, url_for, redirect

import db
import models
import sql
import utils
from data_input.data_input import data_input
from api.api import api


app = Flask(__name__, static_folder="static", template_folder='templates')
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.register_blueprint(data_input, url_prefix='/data_input',
                       static_folder='/static',
                       template_folder='/templates')
app.register_blueprint(api, url_prefix='/api')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/4')
def signup():
    """User sign-up form for account creation."""
    form = models.SignupForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "signup.jinja2",
        form=form,
        template="form-template",
        title="Signup Form"
    )


@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        if username == 'root' and password == 'pass':
            return redirect(url_for('menu'))
        else:
            message = "Неверное имя пользователя или пароль"
    return render_template('login.html', message=message)


@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
    message2 = ''
    dtn = request.args.get('dtn')  # запрос к данным формы
    dtk = request.args.get('dtk')
    if dtn is None:
        dtn = '07.12.2021'
    if dtk is None:
        dtk = '07.12.2021'
    if request.method == 'POST':
        dtn = request.form.get('dtn')  # запрос к данным формы
        dtk = request.form.get('dtk')
        if dtn != '' and dtk != '':
            message2 = "Корректный период"
            return redirect(url_for('report', dtn=dtn, dtk=dtk))
        else:
            message2 = "Некорректный период"
            return redirect(url_for('report', message=message2, dtn=dtn, dtk=dtk))
    sql_select_filtered = sql.sql_select.format(dtn=dtn, dtk=dtk)
    result = db.select(sql_select_filtered)
    return render_template("report_filter.html", my_list=result, message=message2)


@app.route("/report", methods=['GET', 'POST'])
def report():
    message3 = ''
    dtn = request.args.get('dtn')  # запрос к данным формы
    dtk = request.args.get('dtk')
    if request.method == 'POST':
        dtn = request.form.get('dtn')  # запрос к данным формы
        dtk = request.form.get('dtk')
        if dtn != '' and dtk != '':
            message3 = "Корректный период"
            return redirect(url_for('report_filter', dtn=dtn, dtk=dtk))
        else:
            message3 = "Некорректный период"
            return redirect(url_for('report_filter', message=message3, dtn=dtn, dtk=dtk))
    sql_select_filtered = sql.sql_select.format(dtn=dtn, dtk=dtk)
    result = db.select(sql_select_filtered)
    return render_template("report.html", my_list=result)


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
