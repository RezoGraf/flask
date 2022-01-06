from flask import Blueprint, render_template, abort, redirect, url_for, request
# регистрируем схему `Blueprint`
from data_input.models import SignupForm, WtfTemplate, WtfTemplate2, WtfTemplate3
from data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc
from data_input.sql_data_input import sql_ins_it_rasp_duty, sql_upd_it_rasp_duty, sql_del_it_rasp_duty
from data_input.sql_data_input import sql_ins_it_rasp, sql_del_it_rasp
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


@data_input.route('/wtf_start', methods=['GET', 'POST'])
def wtf_start():
    # otd = request.args.get('12')
    # doc = request.args.get('23')

    result_podr2 = db.select(sql.sql_podr)
    result_rasp = db.select(sql.sql_it_rasp.format(doc=0))
    visible_ = ''
    if result_rasp == []:
        result_rasp.append('')
        result_rasp.append('')
        result_rasp.append('')
        result_rasp.append('0')
        result_rasp.append('0')
        result_rasp.append('')
        result_rasp = (result_rasp, )
    else:
        visible_ = 'style=display:none;'
    # result_fio = db.select(sql.sql_fio.format(otd=0))
    # if result_fio == []:
    result_fio=([])
    result_fio.append(0)
    result_fio.append('')
    result_fio = (result_fio, )
    result_podr = db.select(sql.sql_podr_selected.format(otd=0))
    form = WtfTemplate3()
    return render_template('wtf_start.html',
                           form=form,
                           result_rasp=result_rasp,
                           result_podr2=result_podr2,
                           result_fio=result_fio,
                           result_podr=result_podr,
                           visible_=visible_)


@data_input.route('/wtf_template3/', methods=['GET', 'POST'])
def wtf_template3():
    otd = request.args.get('otd')
    result_notd = db.select(sql.sql_podr_selected.format(otd=otd))
    notd = result_notd[0]
    print(result_notd)
    result_doc = db.select(sql.sql_doc.format(otd=otd))
    doc = request.args.get('doc') or utils.list_to_int(result_doc)

    lpu = utils.list_to_int(db.select(sql.sql_lpu_selected.format(otd=otd)))
    result_rasp = db.select(sql.sql_it_rasp.format(doc=doc))
    visible_ = ''
    if result_rasp == []:
        result_rasp.append('')
        result_rasp.append('')
        result_rasp.append('')
        result_rasp.append('0')
        result_rasp.append('0')
        result_rasp.append('')
        result_rasp = (result_rasp, )
    else:
        visible_ = 'style=display:none;'

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
            db.write(sql_upd_it_rasp_duty.format(doc=doc, UpdDtnDuty=UpdDtnDuty, UpdTimeDuty=UpdTimeDuty, UpdNDay=UpdNDay, UpdId=UpdId))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

        if request.form['btn'] == 'DelDuty':
            DelId = request.form.get('DelIdDuty')
            db.write(sql_del_it_rasp_duty.format(DelId=DelId))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc))

        if request.form['btn'] == 'UpdRegimeWork':
            spz = request.form.get('UpdSpz')
            if spz == "":
                spz = 0
            room = request.form.get('UpdRoom')
            if room == "":
                room = 0
            interval1 = request.form.get('UpdNoEvenDay')
            if interval1 == "":
                interval1 = 0
            interval2 = request.form.get('UpdEvenDay')
            if interval2 == "":
                interval2 = 0
            ntv = request.form.get('UpdNtv')
            nlist = request.form.get('UpdNlist')
            visible_ = 'style=display:none;'
            db.write(sql_del_it_rasp.format(doc=doc))
            print(sql_ins_it_rasp.format(doc=doc, lpu=lpu, otd=otd, spz=spz, room=room, interval1=interval1, interval2=interval2, ntv=ntv, nlist=nlist))
            db.write(sql_ins_it_rasp.format(doc=doc, lpu=lpu, otd=otd, spz=spz, room=room, interval1=interval1, interval2=interval2, ntv=ntv, nlist=nlist))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc, visible_=visible_))

        if request.form['btn'] == 'DelRegimeWork':
            visible_ = ''
            db.write(sql_del_it_rasp.format(doc=doc))
            return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc, visible_=visible_))

    result_rsn = db.select(sql.sql_rsp_rsn)
    result_rsp_blc = db.select(sql.sql_rsp_blc.format(doc=doc))
    result_room = db.select(sql.sql_room.format(doc=doc))
    result_spz = db.select(sql.sql_spz)

    result_duty = db.select(sql.sql_it_rasp_duty.format(doc=doc))
    result_time = db.select(sql.sql_interval_time)

    result_fio = db.select(sql.sql_fio.format(otd=otd))
    result_doc = db.select(sql.sql_doctod.format(otd=otd, doc=doc))
    fioSotrudnika = db.select(sql.sql_fio_sotrudnika.format(doc=doc))
    fioSotrudnika = utils.list_to_str(fioSotrudnika)
    result_podr = db.select(sql.sql_podr_selected.format(otd=otd))
    result_podr2 = db.select(sql.sql_podr)

    form = WtfTemplate3()
    print(visible_)
    return render_template('wtf_template3.html',
                           result_fio=result_fio,
                           result_rsn=result_rsn,
                           result_rsp_blc=result_rsp_blc,
                           result_rasp=result_rasp,
                           result_duty=result_duty,
                           result_time=result_time,
                           result_room=result_room,
                           result_spz=result_spz,
                           fioSotrudnika=fioSotrudnika,
                           doc=doc,
                           otd=otd,
                           lpu=lpu,
                           form=form,
                           visible_=visible_,
                           result_podr=result_podr,
                           result_podr2=result_podr2)


@data_input.route('/di_frame_fio', methods=['GET', 'POST'])
def di_frame_fio():
    otd = request.args.get('otd')
    result_podr = db.select(sql.sql_podr_selected.format(otd=otd))
    result_fio = db.select(sql.sql_fio.format(otd=otd))
    result_podr2 = db.select(sql.sql_podr)
    print(result_podr)
    return render_template('wtf_iframe_left.html',
                           result_podr=result_podr,
                           result_podr2=result_podr2,
                           result_fio=result_fio)
    