from flask import Blueprint, render_template, abort, redirect, url_for, request
# регистрируем схему `Blueprint`
from data_input.models import SignupForm, WtfTemplate, WtfTemplate2, WtfTemplate3
from data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc
from data_input.sql_data_input import sql_ins_rsp_blc, sql_ins_it_rasp_duty, sql_upd_it_rasp_duty, sql_del_it_rasp_duty
from . import data_input
import db
import sql
import utils
import calendar
import pandas as pd

data_input = Blueprint('data_input', __name__)

# теперь в этой схеме, вместо экземпляра приложения
# 'app' используем экземпляр `Blueprint` с именем `data_input`.
# Связываем URL со схемой `data_input`


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
        return redirect(url_for('data_input.wtf_template3',
                                otd=otd,
                                doc=doc))
    result_podr = db.select(sql.sql_podr_selected.format(otd=otd))
    result_fio = db.select(sql.sql_fio.format(otd=otd))
    form = WtfTemplate2()
    #Если метод запроса - POST и если поля формы валидны
    return render_template('wtf_template2.html',
                           result_fio=result_fio,
                           result_podr=result_podr,
                           form=form)


@data_input.route('/wtf_template3', methods=['GET', 'POST'])
def wtf_template3():
    otd = request.args.get('otd')
    doc = request.args.get('doc')

    if request.method == 'POST':
        if request.form['btn'] == 'DelRspBlc':
            DelIblc = request.form.get('DelIblc')
            db.write(sql_del_rsp_blc.format(DelIblc=DelIblc))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

        if request.form['btn'] == 'UpdRspBlc':
            UpdIblc = request.form.get('UpdIblc')
            UpdDtn = request.form.get('UpdDtn')
            UpdDtk = request.form.get('UpdDtk')
            UpdRsn = request.form.get('UpdRsn')
            print(UpdRsn, UpdDtk, UpdDtn, UpdIblc)
            db.write(sql_upd_rsp_blc.format(UpdIblc=UpdIblc, UpdDtn=UpdDtn, UpdDtk=UpdDtk, UpdRsn=UpdRsn))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

        if request.form['btn'] == 'InsRspBlc':
            InsDtn = request.form.get('InsDtn')
            InsDtk = request.form.get('InsDtk')
            InsRsn = request.form.get('InsRsn')
            procedure_name = 'NEW_IBLC'
            output_params = db.proc(procedure_name)
            output_params = utils.list_to_int(output_params)
            # print(InsDtn, InsDtk, InsRsn)
            db.write(sql_ins_rsp_blc.format(output_params=output_params, doc=doc, InsDtn=InsDtn, InsDtk=InsDtk, InsRsn=InsRsn))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

        if request.form['btn'] == 'InsDuty':
            InsDtnDuty = request.form.get('InsDtnDuty')
            InsTimeDuty = request.form.get('InsTimeDuty')
            procedure_name = 'NEW_ID_RASP_DUTY'
            output_params = db.proc(procedure_name)
            output_params = utils.list_to_int(output_params)
            df = pd.Timestamp(InsDtnDuty)
            InsNDay = df.dayofweek
            db.write(sql_ins_it_rasp_duty.format(output_params=output_params, doc=doc, InsDtnDuty=InsDtnDuty, InsTimeDuty=InsTimeDuty, InsNDay=InsNDay))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

        if request.form['btn'] == 'UpdDuty':
            UpdId = request.form.get('UpdId')
            UpdDtnDuty = request.form.get('UpdDtnDuty')
            UpdTimeDuty = request.form.get('UpdTimeDuty')
            df = pd.Timestamp(UpdDtnDuty)
            UpdNDay = df.dayofweek
            print(sql_upd_it_rasp_duty.format(doc=doc, UpdDtnDuty=UpdDtnDuty, UpdTimeDuty=UpdTimeDuty, UpdNDay=UpdNDay, UpdId=UpdId))
            # db.write(sql_upd_it_rasp_duty.format(doc=doc, UpdDtnDuty=UpdDtnDuty, UpdTimeDuty=UpdTimeDuty, UpdNDay=UpdNDay, UpdId=UpdId))
            # return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

        if request.form['btn'] == 'DelDuty':
            DelId = request.form.get('DelIdDuty')
            db.write(sql_del_it_rasp_duty.format(DelId=DelId))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

    result_fio = db.select(sql.sql_fio.format(otd=otd))
    result_rsn = db.select(sql.sql_rsp_rsn)
    result_rsp_blc = db.select(sql.sql_rsp_blc.format(doc=doc))
    result_rasp = db.select(sql.sql_it_rasp.format(doc=doc))
    result_duty = db.select(sql.sql_it_rasp_duty.format(doc=doc))
    result_time = db.select(sql.sql_interval_time)

    result_fio = db.select(sql.sql_fio.format(otd=otd))
    result_doc = db.select(sql.sql_doctod.format(otd=otd, doc=doc))
    fioSotrudnika = db.select(sql.sql_fio_sotrudnika.format(doc=doc))
    form = WtfTemplate3()

    #outputParams = list_to_list(output_params)
    # print("Результат генератора: ", output_params)
    return render_template('wtf_template3.html',
                           result_fio=result_fio,
                           result_rsn=result_rsn,
                           result_rsp_blc=result_rsp_blc,
                           result_rasp=result_rasp,
                           result_duty=result_duty,
                           result_time=result_time,
                           fioSotrudnika=fioSotrudnika,
                           form=form)
