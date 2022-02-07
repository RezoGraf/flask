from flask import Blueprint, render_template, abort, redirect, url_for, request, session
# регистрируем схему `Blueprint`
from app.data_input.models import SignupForm, WtfTemplate, WtfTemplate2, WtfTemplate3
from app.data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc
from app.data_input.sql_data_input import sql_ins_it_rasp_duty, sql_upd_it_rasp_duty, sql_del_it_rasp_duty
from app.data_input.sql_data_input import sql_ins_it_rasp, sql_del_it_rasp
from . import data_input
import app.db as db
import app.sql as sql
import app.utils as utils
# import calendar
import pandas as pd
# from dateutil import parser
# from datetime import date
from app.menu_script import generate_menu



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


@data_input.route('/wtf_template3/', methods=['GET', 'POST'])
def wtf_template3():
    if 'arena_mpp' not in session:
        return redirect(url_for("login"))
    else:
        if 'arena_user' in session:
            arena_user = session.get('arena_user')
        else:
            arena_user = 0
            
        result_accessotd = db.select(sql.sql_accessOtd.format(arena_user=arena_user))[0][0] #доступные отделения USERS_SET_APP
        result_accessSdl = db.select(sql.sql_accessSdl.format(arena_user=arena_user))[0][0] #доступные должности
        
        if  result_accessotd != '0':
            select_otd=f' and otd in({result_accessotd})'
            random_otd = db.select(sql.sql_randomOtd.format(select_otd=select_otd)) #первое попавшееся отделение    
        else:
            select_otd = ''
            random_otd = '0'
            
        if  result_accessSdl != '0':
            select_sdl=f' and n_doc.sdl in({result_accessSdl})'
        else:
            select_sdl = ''
            
        otd = request.args.get('otd') or utils.list_to_int(random_otd)  #код выбранного отделения
        lpu = int(db.select(sql.sql_currentOtd.format(otd=otd))[0][2])
        if int(otd) == 0:
            current_otd = ''
        else:
            current_otd = f' and otd={otd}'
        result_fio = db.select(sql.sql_allDoc.format(current_otd = current_otd, select_sdl=select_sdl))#все сотрудники выбранного отделения
        doc = request.args.get('doc') or result_fio[0][0]      #код выбранного сотрудника со wtf_template3 или первый из запроса       
        fioSotrudnika = db.select(sql.sql_fio_sotrudnika.format(doc=doc))[0][0]
        
        result_rasp = db.select(sql.sql_it_rasp.format(doc=doc)) #режим работы сотрудника
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
        result_duty = db.select(sql.sql_it_rasp_duty.format(doc=doc)) #работа в выходные дни
            
        # result_noWork = db.select(sql.sql_noWork.format(doc=doc)) #отсутствие на рабочем месте
        # result_duty = db.select(sql.sql_it_rasp_duty.format(doc=doc)) #работа в выходные дни
        # result_room = db.select(sql.sql_room.format(doc=doc)) #номера кабинетов
        # result_spz = db.select(sql.sql_allSpz) #список специальностей
        # result_rsn = db.select(sql.sql_rsp_rsn) #список причин отсутствия
        # result_time = db.select(sql.sql_interval_time) #интервал времени
        # result_time2 = db.select(sql.sql_interval_time) 
        
        
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
                db.write(sql_upd_it_rasp_duty.format(doc=doc, UpdDtnDuty=InsDtnDuty, UpdTimeDuty=InsTimeDuty, UpdNDay=InsNDay, UpdId=output_params))   
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
                         
                db.write(sql_ins_it_rasp.format(doc=doc, lpu=lpu, otd=otd, spz=spz, room=room, interval1=interval1, interval2=interval2, ntv=ntv, nlist=nlist))
                return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc, visible_=visible_ ))

            if request.form['btn'] == 'DelRegimeWork':
                visible_ = ''
                db.write(sql_del_it_rasp.format(doc=doc))
                return redirect(url_for("data_input.wtf_template3", otd=otd, doc=doc, visible_=visible_))
 
        result_room = db.select(sql.sql_room.format(doc=doc)) #номера кабинетов
        result_spz = db.select(sql.sql_allSpz) #список специальностей
        result_rsn = db.select(sql.sql_rsp_rsn) #список причин отсутствия
        result_time = db.select(sql.sql_interval_time) #интервал времени
        result_time2 = db.select(sql.sql_interval_time)   
                                  
        result_noWork = db.select(sql.sql_noWork.format(doc=doc)) #отсутствие на рабочем месте
                
        result_podr = db.select(sql.sql_currentOtd.format(otd=otd)) #список отделений
        result_podr2 = db.select(sql.sql_allOtd.format(select_otd=select_otd)) #список отделений
        
        idx = 0     
        for x in result_podr2 :            
            if x[0] == int(otd) :
              break
            idx +=1  
        else: pass             

        notd = result_podr2.pop(idx)

        form = WtfTemplate3()
        if 'arena_fio' in session:
            arena_fio = session.get('arena_fio')
        else:
            arena_fio = "Не пользователь домена"

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
                            notd=notd[1],
                            lpu=lpu,
                            form=form,
                            visible_=visible_,
                            result_podr=result_podr,
                            result_podr2=result_podr2,
                            arena_fio=arena_fio)
    