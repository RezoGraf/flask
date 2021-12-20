from flask import Flask, render_template, request, url_for, redirect
from flask import Flask, render_template
from flask import request
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from flask_wtf import Form
from wtforms import SelectField
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
db = SQLAlchemy(app)


#  категория
class Category(db.Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(1024))

    def __repr__(self):
        return '<Category %s>' % self.name

    def __unicode__(self):
        return self.name


#  подкатегория
class SubCategory(db.Model):
    __tablename__ = 'sub_category'
    id = Column(Integer, primary_key=True)
    name = Column(String(1024))
    category_id = db.Column(Integer, ForeignKey('category.id'))
    category = db.relationship("Category", backref="Ctegory.id")

    def __repr__(self):
        return '<SubCategory %s>' % self.name

    def __unicode__(self):
        return self.name

#  создание таблиц
db.create_all()
#  заполнение базы
#  если записи отсутствуют
if len(Category.query.all()) is 0:
    for name in ['фрукты', 'напитки', 'молочные продукты']:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()

if len(SubCategory.query.all()) is 0:
    for name in ['апельсины', 'яблоки', 'груши']:
        sub_category = SubCategory(category_id=1, name=name)
        db.session.add(sub_category)

    for name in ['сок', 'вода', 'газировка']:
        sub_category = SubCategory(category_id=2, name=name)
        db.session.add(sub_category)

    for name in ['молоко', 'сметана', 'масло']:
        sub_category = SubCategory(category_id=3, name=name)
        db.session.add(sub_category)
    db.session.commit()


class FormCategory(Form):
    category = SelectField(u'Категория', coerce=int)
    sub_category = SelectField(u'Под категория', coerce=int)

    def __init__(self, *args, **kwargs):
        super(FormCategory, self).__init__(*args, **kwargs)
        self.category.choices = \
            [(g.id, u"%s" % g.name) for g in Category.query.order_by('name')]
        #  выбранное поле по умолчанию
        self.category.choices.insert(0, (0, u"Не выбрана"))

        self.sub_category.choices = list()
        #  выбранное поле по умолчанию
        self.sub_category.choices.insert(0, (0, u"Не выбрана"))


@app.route('/6')
def index():
    form = FormCategory()
    return render_template('index2.html',
                           form=form
                           )


@app.route('/get_sub_category', methods=('GET', 'POST'))
def get_sub_category():
    category_id = request.form['category']
    item_list = SubCategory.query.filter_by(category_id=category_id).all()
    result_list = dict()
    for item in item_list:
        result_list[item.id] = item.name
    return json.dumps(result_list)

if __name__ == '__main__':
    app.run(debug=True)


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
