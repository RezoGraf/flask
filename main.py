import flask
import fdb
from flask import Flask, render_template, url_for, redirect, request
import os
from flask_login import LoginManager
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField
from wtforms.validators import ValidationError, DataRequired, \
    Email, EqualTo, Length


app = Flask(__name__, static_folder="static", template_folder='templates')
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'


def db_select(sql):
    con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB',
                      user='sysdba', password='masterkey', charset="utf-8")
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


def db_write(sql):
    con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB',
                      user='sysdba', password='masterkey', charset="utf-8")
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


sql_select = """SELECT  (
SELECT  SNLPU
FROM N_LPU
WHERE N_DOC.LPU=N_LPU.LPU
AND N_LPU.TER=5), (select nmpp from n_mpp where n_mpp.mpp=n_doc.mpp) as NDOC, (
SELECT  NRSN
FROM RSP_RSN
WHERE RSP_RSN.RSN=RSP_BLC.RSN), RSP_BLC.DTN , RSP_BLC.DTK
FROM RSP_BLC, N_DOC
WHERE (RSP_BLC.DOC=N_DOC.DOC)
AND (RSP_BLC.DTK>='{dtn}' AND RSP_BLC.DTK<='{dtk}')"""


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


@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


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


class CreateUserForm(FlaskForm):

    username = StringField(label=('Username'),
                           validators=[DataRequired(),
                                       Length(max=64)])
    email = StringField(label=('Email'),
                        validators=[DataRequired(),
                                    Email(),
                                    Length(max=120)])
    password = PasswordField(label=('Password'),
                             validators=[DataRequired(),
                                         Length(min=8, message='Password should be at least %(min)d characters long')])
    confirm_password = PasswordField(
        label=('Confirm Password'),
        validators=[DataRequired(message='*Required'),
                    EqualTo('password', message='Both password fields must be equal!')])
    receive_emails = BooleanField(label=('Receive merketting emails.'))
    submit = SubmitField(label=('Submit'))


class UserRegistrationForm(FlaskForm):
    # ...
    submit = SubmitField(label=('Submit'))

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&amp;/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")


class WtfTemplate2(FlaskForm):
    submit = SubmitField(label=('Submit'))


def list_to_list(list_result):
    for s in list_result:
        string_result = ''.join(str(e) for e in list_result)
        string_result = string_result.replace('(', '')
        string_result = string_result.replace(')', '')
        string_result = string_result.replace(',', '')
#    string_result = int(string_result)
        string_result = string_result.append(s)
    return string_result


@app.route('/wtf_template', methods=('GET', 'POST'))
def wtf_template():
    if request.method == 'POST':
        otd = request.form.get('otd')
        return redirect(url_for('wtf_template2', otd=otd))
    sql_podr = "select otd,notd from np_otd where notd is not null"
    result_podr = db_select(sql_podr)
    print(result_podr)
    print(type(result_podr))
    form = CreateUserForm()
    #Если метод запроса - POST и если поля формы валидны
    if form.validate_on_submit():
        return f'''<h1> Welcome {form.username.data} </h1>'''
    return render_template('wtf_template.html', result_podr=result_podr,  form=form)


@app.route('/wtf_template2', methods=('GET', 'POST'))
def wtf_template2():
    otd = request.args.get('otd')
    if request.method == 'POST':
        doc = request.form.get('doc')
        return redirect(url_for('wtf_template3', otd=otd, doc=doc))
    sql_fio = f"""select doc, ndoc from n_doc where pv=1 and otd='{otd}'"""
    result_fio = db_select(sql_fio)
    print(result_fio)
    form = WtfTemplate2()
    #Если метод запроса - POST и если поля формы валидны
    con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB',
                      user='sysdba', password='masterkey', charset="utf-8")
    cur = con.cursor()
    s = cur.callproc('NEW_IBLC')
    outputParams = cur.fetchone()
    print(outputParams)
    print("Результат генератора: ", s)
    return render_template('wtf_template2.html', result_fio=result_fio, form=form)


@app.route('/wtf_template3', methods=('GET', 'POST'))
def wtf_template3():
    otd = request.args.get('otd')
    doc = request.args.get('doc')
    if request.method == 'POST':
        doc = request.form.get('doc')
        return redirect(url_for('wtf_template3', otd=otd, doc=doc))
    sql_fio = f"""select doc, ndoc from n_doc where pv=1 and otd='{otd}'"""
    result_fio = db_select(sql_fio)
    print(result_fio)
    form = WtfTemplate2()
    #Если метод запроса - POST и если поля формы валидны
    #cur.callproc("NEW_IBLC", (input1, input2))
    return render_template('wtf_template2.html', result_fio=result_fio, form=form)



if __name__ == '__main__':
    app.run(host="localhost", port="5000")
