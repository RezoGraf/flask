from flask import Blueprint, render_template, abort, redirect, url_for, request
from jinja2 import TemplateNotFound
# регистрируем схему `Blueprint`
from data_input.models import SignupForm, WtfTemplate, WtfTemplate2, WtfTemplate3
from data_input.sql_data_input import sql_ins_rsp_blc

from . import data_input
import db
import sql
import utils

data_input = Blueprint('data_input', __name__)

# теперь в этой схеме, вместо экземпляра приложения
# 'app' используем экземпляр `Blueprint` с именем `data_input`.
# Связываем URL со схемой `data_input`


@data_input.route('/2')
def index():
    return "This is an example app"


# @data_input.route('/1', methods=['GET', 'POST'])
# def signup():
#     try:
#         """User sign-up form for account creation."""
#         form = models.SignupForm()
#         if form.validate_on_submit():
#             return redirect(url_for("success"))
#         return render_template(
#             "signup.jinja2",
#             form=form,
#             template="form-template",
#             title="Signup Form"
#         )
#     except TemplateNotFound:
#         abort(404)


@data_input.route('/signup', methods=['GET', 'POST'])
def signup():
    """User sign-up form for account creation."""
    form = SignupForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template(
        "signup.jinja2",
        form=form,
        template="form-template",
        title="Signup Form"
    )


@data_input.route('/', methods=('GET', 'POST'))
def wtf_template():
    if request.method == 'POST':
        otd = request.form.get('otd')
        return redirect(url_for('data_input.wtf_template2', otd=otd))
    result_podr = db.select(sql.sql_podr)
    form = WtfTemplate()
    #Если метод запроса - POST и если поля формы валидны
    # if form.validate_on_submit():
    #     return f'''<h1> Welcome {form.username.data} </h1>'''
    # if form.validate_on_submit():
    #     name=Name(form.name.data,form.groupID.data)
    #     db.session.add(name)
    #     db.session.commit()
    #     return "New name added"
    return render_template('wtf_template.html',
                           result_podr=result_podr,
                           form=form,
                           title="Выбор подразделения")


@data_input.route('/wtf_template2', methods=('GET', 'POST'))
def wtf_template2():
    otd = request.args.get('otd')
    if request.method == 'POST':
        doc = request.form.get('doc')
        return redirect(url_for('data_input.wtf_template3', otd=otd, doc=doc))
    result_podr = db.select(sql.sql_podr)
    result_fio = db.select(sql.sql_fio.format(otd=otd))
    form = WtfTemplate2()
    #Если метод запроса - POST и если поля формы валидны
    return render_template('wtf_template2.html', result_fio=result_fio, result_podr=result_podr, form=form)


@data_input.route('/wtf_template3', methods=['GET', 'POST'])
def wtf_template3():
    otd = request.args.get('otd')
    doc = request.args.get('doc')
    if request.method == 'POST':
        # doc = request.form.get('doc')
        dtn = request.form.get('dtn')
        dtk = request.form.get('dtk')
        procedure_name = 'NEW_IBLC'
        output_params = db.proc(procedure_name)
        output_params = utils.list_to_int(output_params)
        print(sql_ins_rsp_blc.format(output_params=output_params,doc=doc,dtn=dtn,dtk=dtk))
        db.write(sql_ins_rsp_blc.format(output_params=output_params,doc=doc,dtn=dtn,dtk=dtk))

        return "ok"
        # return redirect(url_for('wtf_template3', otd=otd, doc=doc))

    result_fio = db.select(sql.sql_fio.format(otd=otd))
    form = WtfTemplate3()

    #outputParams = list_to_list(output_params)
    # print("Результат генератора: ", output_params)
    return render_template('wtf_template3.html', result_fio=result_fio, form=form)
