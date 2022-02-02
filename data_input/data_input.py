from flask import Blueprint, render_template, abort, redirect, url_for, request, session
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
from dateutil import parser
from datetime import date
from menu_script import generate_menu



data_input = Blueprint('data_input', __name__)

# теперь в этой схеме, вместо экземпляра приложения
# 'app' используем экземпляр `Blueprint` с именем `data_input`.
# Связываем URL со схемой `data_input`


@data_input.route('/', methods=('GET', 'POST'))
def wtf_template():
        
    if request.method == 'POST':
        otd = request.form.get('otd')
        return redirect(url_for('data_input.wtf_template2', otd=otd))
    result_podr = db.select(sql.sql_allOtd)
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
    result_podr = db.select(sql.sql_currentOtd.format(otd=otd))
    result_fio = db.select(sql.sql_allDoc.format(otd=otd))
    form = WtfTemplate2()
    #Если метод запроса - POST и если поля формы валидны
    return render_template('wtf_template2.html',
                           result_fio=result_fio,
                           result_podr=result_podr,
                           form=form)


@data_input.route('/wtf_template3', methods=['GET', 'POST'])
def wtf_template3():
    if 'arena_mpp' in session:
        if 'arena_user' in session:
            arena_user = session.get('arena_user')
        else:
            arena_user = 0
        result_accessotd = db.select(sql.sql_accessOtd.format(arena_user=arena_user))[0][0]
        result_accessSdl = db.select(sql.sql_accessSdl.format(arena_user=arena_user))[0][0]
        
        if  result_accessotd != '0':
            select_otd=f' and otd in({result_accessotd})'
        else:
            select_otd = ''
            
        if  result_accessSdl != '0':
            select_sdl=f' and n_doc.sdl in({result_accessSdl})'
        else:
            select_sdl = ''    
        
        result_otd = db.select(sql.sql_randomOtd.format(select_otd=select_otd))
        otd = request.args.get('otd') or utils.list_to_int(result_otd)  
        result_notd = db.select(sql.sql_currentOtd.format(otd=otd))

        notd = result_notd[0]
        
        result_doc = db.select(sql.sql_randomDoc.format(otd=otd))
        doc = request.args.get('doc') or utils.list_to_int(result_doc)

        lpu = int(db.select(sql.sql_currentOtd.format(otd=otd))[0][2])
        result_rasp = db.select(sql.sql_it_rasp.format(doc=doc))
        visible_ = ''
        if result_rasp == []:
            result_rasp.append('0') #ROOM
            result_rasp.append('')  #NROOM_KR
            result_rasp.append('0') #ID_INTERVAL1
            result_rasp.append('')  #NOEVEN_DAY
            result_rasp.append('0') #ID_INTERVAL2
            result_rasp.append('')  #EVEN_DAY
            result_rasp.append('0') #NTV
            result_rasp.append('0') #NLIST
            result_rasp.append('0') #SPZ
            result_rasp.append('')  #NSPZ
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
                print(interval2) 
                
                ntv = request.form.get('UpdNtv')
                nlist = request.form.get('UpdNlist')
                visible_ = 'style=display:none;'
                db.write(sql_del_it_rasp.format(doc=doc))
                
                print(sql_ins_it_rasp.format(doc=doc, lpu=lpu, otd=otd, spz=spz, room=room, interval1=interval1, interval2=interval2, ntv=ntv, nlist=nlist))
            
                db.write(sql_ins_it_rasp.format(doc=doc, lpu=lpu, otd=otd, spz=spz, room=room, interval1=interval1, interval2=interval2, ntv=ntv, nlist=nlist))
                return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc, visible_=visible_ ))

            if request.form['btn'] == 'DelRegimeWork':
                visible_ = ''
                db.write(sql_del_it_rasp.format(doc=doc))
                return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc, visible_=visible_))

        result_rsn = db.select(sql.sql_rsp_rsn)
        
        result_noWork = db.select(sql.sql_noWork.format(doc=doc))
        
        result_room = db.select(sql.sql_room.format(doc=doc))
        result_spz = db.select(sql.sql_allSpz)

        result_duty = db.select(sql.sql_it_rasp_duty.format(doc=doc))
        result_time = db.select(sql.sql_interval_time)
        result_time2 = db.select(sql.sql_interval_time)

        result_fio = db.select(sql.sql_allDoc.format(otd=otd, select_sdl=select_sdl))
        
        result_doc = db.select(sql.sql_doctod.format(otd=otd, doc=doc))
        fioSotrudnika = db.select(sql.sql_fio_sotrudnika.format(doc=doc))
        fioSotrudnika = utils.list_to_str(fioSotrudnika)
        result_podr = db.select(sql.sql_currentOtd.format(otd=otd))
        result_podr2 = db.select(sql.sql_allOtd.format(select_otd=select_otd))

        form = WtfTemplate3()
        if 'arena_fio' in session:
            arena_fio = session.get('arena_fio')
        else:
            arena_fio = "Не пользователь домена"

        print(visible_)
        menu = generate_menu()
        return render_template('wtf_template3.html',
                            menu = menu,
                            result_fio=result_fio,
                            result_rsn=result_rsn,
                            result_rsp_blc=result_noWork,
                            result_rasp=result_rasp,
                            result_duty=result_duty,
                            result_time=result_time,
                            result_time2=result_time2,
                            result_room=result_room,
                            result_spz=result_spz,
                            fioSotrudnika=fioSotrudnika,
                            doc=doc,
                            otd=otd,
                            lpu=lpu,
                            form=form,
                            visible_=visible_,
                            result_podr=result_podr,
                            result_podr2=result_podr2,
                            arena_fio=arena_fio)
    else :
        return redirect(url_for("app.login"))
    

@data_input.route('/wtf_template4/', methods=['GET', 'POST'])
def WtfTemplate4():
    # otd = request.args.get('otd')
    # if otd is None : otd=12
    # # result_podr = db.select(sql.sql_currentOtd.format(otd=otd))
    # result_fio = db.select(sql.sql_allDoc.format(otd=otd))
    otd=12  
  
    current_date = date.today()
    # current_date_string = current_date.strftime('%m/%d/%y')   
    current_year = parser.parse(current_date.strftime('%m/%d/%y')).strftime("%Y")
    current_month = parser.parse(current_date.strftime('%m/%d/%y')).strftime("%m")
    all_day = calendar.monthrange(int(current_year), int(current_month))[1]
    result_otd = db.select(sql.sql_allOtd) 
    russianDayWeek = {'Mon':'Пн.' , 'Tue':'Вт.' , 'Wed':'Ср.' , 'Thu':'Чт.' , 'Fri':'Пт.' , 'Sat':'Сб.' , 'Sun':'Вс.'}
    
    result_th = {}
    for i in range(all_day):
            i+=1
            dt = f'{str(current_month)}.{str(i)}.{str(current_year)}'
            ans = parser.parse(dt).strftime("%a")
            pa = russianDayWeek[ans]
            if i<10 :
                p=f'0{i}'
            else:
                p=str(i)  
            value_ = f'{p} <br> {pa}' 
            key_ = f'day{str(i)}'
            result_th[key_] = value_        
        
    print(result_th)
    if request.method == 'POST':
        result_fio = db.select(sql.sql_allDoc.format(otd=otd))
        result_otd = db.select(sql.sql_allOtd)
        otd=request.form.get('OTD')
        otd=12
        current_year=request.form.get('year')
        current_month=request.form.get('month')
        all_day = calendar.monthrange(int(current_year), int(current_month))[1]
        result_th = {}
        for i in range(all_day):
            i+=1
            dt = f'{str(current_month)}.{str(i)}.{str(current_year)}'
            ans = parser.parse(dt).strftime("%a")
            pa = russianDayWeek[ans]
            if i<10 :
                p=f'0{i}'
            else:
                p=str(i)  
            value_ = f'{p} <br> {pa}' 
            key_ = f'day{str(i)}'
            result_th[key_] = value_ 
            
        result_TabelWorkTime = db.select(sql.sql_TabelWorkTime.format(otd=otd, EYear=current_year, EMonth=current_month))
        return render_template('wtf_template4.html',
                               result_otd=result_otd,
                               result_th = result_th,
                               result_TabelWorkTime=result_TabelWorkTime)
        
    result_TabelWorkTime = db.select(sql.sql_TabelWorkTime.format(otd=otd, EYear=current_year, EMonth=current_month))         
    return render_template('wtf_template4.html',
                           result_otd = result_otd,
                           result_th = result_th,
                           result_TabelWorkTime = result_TabelWorkTime)
                        #    result_podr=result_podr,
                        #    result_podr2=result_podr2,
                        
    
    
@data_input.route('/di_frame_fio', methods=['GET', 'POST'])
def di_frame_fio():
    otd = request.args.get('otd')
    result_podr = db.select(sql.sql_currentOtd.format(otd=otd))
    result_fio = db.select(sql.sql_allDoc.format(otd=otd))
    result_podr2 = db.select(sql.sql_allOtd)
    print(result_podr)
    return render_template('wtf_iframe_left.html',
                           result_podr=result_podr,
                           result_podr2=result_podr2,
                           result_fio=result_fio)
    