from flask import render_template, url_for, redirect, request

import models
import sql
from ksp import app
from ksp.db import db_proc, db_select


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        if username == 'root' and password == 'pass':
            # message = "Correct username and password"
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
    sql_select_filtered = sql_select.format(dtn=dtn, dtk=dtk)
    result = db_select(sql_select_filtered)
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
    sql_select_filtered = sql_select.format(dtn=dtn, dtk=dtk)
    print(sql_select_filtered)
    result = db_select(sql_select_filtered)
    return render_template("report.html", my_list=result)


@app.route('/wtf_template', methods=('GET', 'POST'))
def wtf_template():
    if request.method == 'POST':
        otd = request.form.get('otd')
        return redirect(url_for('wtf_template2', otd=otd))
    result_podr = db_select(sql.sql_podr)
    print(result_podr)
    print(type(result_podr))
    form = CreateUserForm()
    # Если метод запроса - POST и если поля формы валидны
    if form.validate_on_submit():
        return f'''<h1> Welcome {form.username.data} </h1>'''
    return render_template('wtf_template.html', result_podr=result_podr, form=form)


@app.route('/wtf_template2', methods=('GET', 'POST'))
def wtf_template2():
    otd = request.args.get('otd')
    if request.method == 'POST':
        doc = request.form.get('doc')
        return redirect(url_for('wtf_template3', otd=otd, doc=doc))
    # sql_fio = f"""select doc, ndoc from n_doc where pv=1 and otd='{otd}'"""
    result_fio = db_select(sql.sql_fio.format(otd))
    print(result_fio)
    form = models.WtfTemplate2()
    procedure_name = 'NEW_IBLC'
    outputParams = db_proc(procedure_name)
    print(outputParams)
    print("Результат генератора: ", s)
    return render_template("wtf_template2.html", result_fio=result_fio, form=form)


@app.route('/wtf_template3', methods=('GET', 'POST'))
def wtf_template3():
    otd = request.args.get('otd')
    doc = request.args.get('doc')
    if request.method == 'POST':
        doc = request.form.get('doc')
        return redirect(url_for('wtf_template3', otd=otd, doc=doc))
    # sql_fio = f"""select doc, ndoc from n_doc where pv=1 and otd='{otd}'"""
    result_fio = db_select(sql.sql_fio.format(otd))
    print(result_fio)
    form = WtfTemplate2()
    # Если метод запроса - POST и если поля формы валидны
    # cur.callproc("NEW_IBLC", (input1, input2))
    return render_template('wtf_template2.html', result_fio=result_fio, form=form)
