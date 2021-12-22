import db
import models
import sql
from api.api import api
from data_input.data_input import data_input
from excel.excel import excel
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
    dtn = request.args.get('dtn')  # запрос к данным формы
    dtk = request.args.get('dtk')
    if dtn is None:
        dtn = '01.12.2021'
    if dtk is None:
        dtk = '07.12.2021'
    if request.method == 'POST':
        dtn = request.form.get('dtn')  # запрос к данным формы
        dtk = request.form.get('dtk')
        return redirect(url_for('report_filter',
                                dtn=dtn,
                                dtk=dtk))
    sql_select_filtered = sql.sql_select.format(dtn=dtn,
                                                dtk=dtk)
    result = db.select(sql_select_filtered)
    print(type(result))
    return render_template("report_filter.html",
                           my_list=result, dtn=dtn, dtk=dtk)


@app.route("/report", methods=['GET', 'POST'])
def report():
    dtn = request.args.get('dtn')  # запрос к данным формы
    dtk = request.args.get('dtk')
    if dtn is None:
        dtn = '01.12.2021'
    if dtk is None:
        dtk = '07.12.2021'
    if request.method == 'POST':
        dtn = request.form.get('dtn')  # запрос к данным формы
        dtk = request.form.get('dtk')
        return redirect(url_for('report',
                                dtn=dtn,
                                dtk=dtk))
    # sql_select_filtered = sql.sql_select.format(dtn=dtn,
    #                                             dtk=dtk)
    result = db.select(sql.sql_select.format(dtn=dtn,
                                                dtk=dtk))
    print(type(result))
    return render_template("report.html",
                           my_list=result, dtn=dtn, dtk=dtk)


if __name__ == "__main__":
    # app.run(host='192.168.100.142', port=80, debug=True)
    app.run('0.0.0.0')
