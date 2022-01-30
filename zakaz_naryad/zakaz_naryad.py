
from werkzeug.wrappers import response
import db
import sql
from api.api import api
from data_input.data_input import data_input
from flask import render_template, request, url_for, redirect, Blueprint
# регистрируем схему `Blueprint`
from data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc
from data_input.sql_data_input import sql_ins_rsp_blc, sql_ins_it_rasp_duty
from . import zakaz_naryad
import pandas as pd
from datetime import datetime


zakaz_naryad = Blueprint('zakaz_naryad', __name__)


@zakaz_naryad.route('/', methods=['GET', 'POST'])
def main():
        if request.method == 'POST':
                
            dtn = request.form.get('dtn_get')
            dtk = request.form.get('dtk_get')
            check_open = request.form.get('check_open')
            check_close = request.form.get('check_close')
            return redirect(url_for('zakaz_naryad.main', dtn=dtn, dtk=dtk, check1=check_open, check2=check_close))
    
        else:
            check_open = request.args.get('check1')
            check_close = request.args.get('check2')
            dtn_simple = request.args.get('dtn')
            dtk_simple = request.args.get('dtk')
            dtn = request.args.get('dtn')  # запрос к данным формы
            dtk = request.args.get('dtk')
 
            if dtn is None:
                dtn = datetime.today().strftime('%d.%m.%Y')
                dtn_simple = datetime.today().strftime('%Y-%m-%d')
            if dtn_simple is None:
                dtn_simple  = datetime.today().strftime('%Y-%m-%d')
            if dtk is None:
                dtk_simple = datetime.today().strftime('%Y-%m-%d')
                dtk = datetime.today().strftime('%d.%m.%Y')
            if dtk_simple is None:
                dtk_simple = datetime.today().strftime('%Y-%m-%d')
                
            if check_open and check_close:
                # print('open and close')
                result = db.select(sql.sql_zakaz_naryad_select.format(dtn=dtn, dtk=dtk))
                return render_template("zakaz_naryad.html",
                                my_list=result, dtn_get=dtn_simple, dtk_get=dtk_simple, check1=check_open, check2=check_close)

            if check_open is None and check_close:
                # print('close')
                result = db.select(sql.sql_zakaz_naryad_select_close.format(dtn=dtn, dtk=dtk))
                return render_template("zakaz_naryad.html",
                                my_list=result, dtn_get=dtn_simple, dtk_get=dtk_simple, check1=check_open, check2=check_close)
                
            if check_open and check_close is None:
                # print('open')
                result = db.select(sql.sql_zakaz_naryad_select_open.format(dtn=dtn, dtk=dtk))
                return render_template("zakaz_naryad.html",
                                my_list=result, dtn_get=dtn_simple, dtk_get=dtk_simple, check1=check_open, check2=check_close)
            else:
                # print('default')
                result = db.select(sql.sql_zakaz_naryad_select.format(dtn=dtn, dtk=dtk))
                return render_template("zakaz_naryad.html", 
                                    my_list=result, dtn_get=dtn_simple, dtk_get=dtk_simple, check1='checked', check2='')
#Наряд-------------------------------------------------------------------------------------------------------------------------                 
@zakaz_naryad.route('/zn_naryad', methods=['GET', 'POST'])
def zn_naryad():
        
    if request.method == 'POST':
        idkv = request.form.get('idkv')
        result = db.select(sql.sql_zn_naryad_select_info.format(idkv=idkv))
        result_usl = db.select(sql.sql_zn_naryad_select_usl.format(idkv=idkv))
        return redirect(url_for('zakaz_naryad.zn_naryad', result_usl = result_usl, zn_naryad_list=result, idkv=idkv))    
   
    else:
        idkv = request.args.get('idkv')    
        result = db.select(sql.sql_zn_naryad_select_info.format(idkv=idkv))
        result_usl = db.select(sql.sql_zn_naryad_select_usl.format(idkv=idkv))        
        return render_template('zn_naryad.html', result_usl = result_usl, zn_naryad_list=result, idkv=idkv)
#Модальное на редактирование наряда-------------------------------------------------------------------------------------------- 
@zakaz_naryad.route('/zn_modal_edit', methods=['GET', 'POST'])
def zn_modal_edit():
        
    if request.method == 'POST':
        idkv = request.args.get('idkv')
        nom_nteh = request.args.get("nom_nteh")
        nom_nlit = request.args.get("nom_nlit")
        nom_npolir = request.args.get("nom_npolir")
        nom_nvarh = request.args.get("nom_nvarh")
        result = db.select(sql.sql_zn_naryad_select_info.format(idkv=idkv))
        return redirect(url_for('zakaz_naryad.zn_modal_edit', zn_naryad_list=result, idkv=idkv, nom_nteh=nom_nteh,
                                nom_nlit=nom_nlit, nom_npolir=nom_npolir, nom_nvarh=nom_nvarh))    
   
    else:
        idkv = request.args.get('idkv')
        nom_nteh = request.args.get("nom_nteh")
        nom_nlit = request.args.get("nom_nlit")
        nom_npolir = request.args.get("nom_npolir")
        nom_nvarh = request.args.get("nom_nvarh")
        result = db.select(sql.sql_zn_naryad_select_info.format(idkv=idkv))
        nteh_db = db.select(sql.sql_zn_naryad_select_teh)
        nlit_db = db.select(sql.sql_zn_naryad_select_lit)
        npol_db = db.select(sql.sql_zn_naryad_select_pol)
        nvar_db = db.select(sql.sql_zn_naryad_select_var)
           
        # nteh_list = list('',)
        # sel_1 = ['<option value="0">Не назначено</option>', ] 
        # for nteh_vol in nteh_db:
        #     nteh_list.append(nteh_vol)
        # for i in range(1, len(nteh_list)):
        #     sel_1_vol = f"""<option value="{nteh_list[i][0]}">{nteh_list[i][1]}</option>"""
        #     sel_1.append(sel_1_vol)
        # for i in range(1, len(sel_1)):   
        #     if str(nom_nteh) in sel_1[i]:
        #         sel_1[i] = f"""<option value="{nom_nteh}" selected>{nteh_list[i][1]}</option>"""
        

        sel_1 = ['<option value="0">Не назначен</option>', ] 
        for i in range(1, len(nteh_db)):
            sel_1_vol = f"""<option value="{nteh_db[i][0]}">{nteh_db[i][1]}</option>"""
            sel_1.append(sel_1_vol)
        for i in range(1, len(sel_1)):   
            if str(nom_nteh) in sel_1[i]:
                sel_1[i] = f"""<option value="{nom_nteh}" selected>{nteh_db[i][1]}</option>"""
                
        sel_2 = ['<option value="0">Не назначен</option>', ] 
        for i in range(1, len(nlit_db)):
            sel_2_vol = f"""<option value="{nlit_db[i][0]}">{nlit_db[i][1]}</option>"""
            sel_2.append(sel_2_vol)
        for i in range(1, len(sel_2)):   
            if str(nom_nlit) in sel_2[i]:
                sel_2[i] = f"""<option value="{nom_nlit}" selected>{nlit_db[i][1]}</option>"""
                
        sel_3 = ['<option value="0">Не назначен</option>', ] 
        for i in range(1, len(npol_db)):
            sel_3_vol = f"""<option value="{npol_db[i][0]}">{npol_db[i][1]}</option>"""
            sel_3.append(sel_3_vol)
        for i in range(1, len(sel_3)):   
            if str(nom_npolir) in sel_3[i]:
                sel_3[i] = f"""<option value="{nom_npolir}" selected>{npol_db[i][1]}</option>"""
        
        sel_4 = ['<option value="0">Не назначен</option>', ] 
        for i in range(1, len(nvar_db)):
            sel_4_vol = f"""<option value="{nvar_db[i][0]}">{nvar_db[i][1]}</option>"""
            sel_4.append(sel_4_vol)
        for i in range(1, len(sel_4)):   
            if str(nom_nvarh) in sel_4[i]:
                sel_4[i] = f"""<option value="{nom_nvarh}" selected>{nvar_db[i][1]}</option>"""
                
        response = f"""<div id="modal-backdrop" class="modal-backdrop fade show" style="display:block;"></div>
                        <div id="modal" class="modal fade show" tabindex="-1" style="display:block;">
                            <div class="modal-dialog modal-dialog-centered modal-lg">
                            <div class="modal-content">
                                <div class="modal-header">
                                <h5 class="modal-title">{result}</h5>
                                <h5 class="modal-title">{nom_nteh} {nom_nlit} {nom_npolir} {nom_nvarh}</h5>                                
                                </div>
                                <div class="modal-body">
                                    <form method="POST">    
                                        <table class="table table-borderless">
                                            <tr>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="tehnik_select">Зубной техник</label> 
                                                    <select class="custom-select" id="tehnik_select">                                                
                                                        {sel_1}
                                                    </select>
                                                </td>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="lit_select">Литейщик</label>
                                                    <select class="custom-select" id="lit_select">                                                
                                                        {sel_2}
                                                    </select>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="polir_select">Полировщик</label>
                                                    <select class="custom-select" id="polir_select">
                                                        {sel_3}
                                                    </select>
                                                </td>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="varh_select">Варщик</label>
                                                    <select class="custom-select" id="varh_select">
                                                        {sel_4}
                                                    </select>
                                                </td>
                                            </tr>
                                        </table>
                                    </form>    
                                </div>
                                <div class="modal-footer">
                                    <table class="table table-borderless">
                                        <tr>
                                            <td style="text-align: left;">
                                                <button type="button" class="btn btn-success" onclick="closeModal()">Сохранить</button>
                                            </td>                                            
                                            <td style="text-align: right;"> 
                                                <button type="button" class="btn btn-danger" onclick="closeModal()">&nbsp;Отмена&nbsp;</button> 
                                            </td>                                            
                                        </tr>
                                </div>
                            </div>
                            </div>
                        </div>"""
        return response
    
# Модальное на закрытие---------------------------------------------------------------------------------------------------------------------------------
@zakaz_naryad.route('/zn_modal_close', methods=['GET', 'POST'])
def zn_modal_close():
        
    if request.method == 'POST':
        idkv = request.args.get('idkv')
        nkv = request.args.get('nkv')
        return redirect(url_for('zakaz_naryad.zn_modal_close', idkv=idkv, nkv=nkv))    
   
    else:
        idkv = request.args.get('idkv')
        nkv = request.args.get('nkv')
        dt_close = request.form.get('dt_close')
        dt_today = datetime.today().strftime('%Y-%m-%d')
        response = f"""<div id="modal-backdrop1" class="modal-backdrop fade show" style="display:block;"></div>
                        <div id="modal1" class="modal fade show" tabindex="-1" style="display:block;">
                            <div class="modal-dialog modal-dialog-centered">
                            <div class="modal-content">
                                <div class="modal-header align-self-center">
                                    <div class="row">
                                        <div class="col align-self-center">
                                            <h4 class="modal-title">Закрытие наряда № {nkv}</h4>
                                        </div>
                                    </div>                            
                                </div>
                                <div class="modal-body" style="text-align: center;">
                                
                                    <form method="POST">
                                        <input type="date" value="{dt_today}" name="dt_close" />
                                    </form>   
                                     
                                </div>
                                <div class="modal-footer">
                                    <table class="table table-borderless">
                                        <tr>
                                            <td style="text-align: left;">
                                                <button 
                                                    hx-get="zn_modal_close_btn?idkv={idkv}&dt_close={dt_close}" 
                                                    hx-target="#modals-here1" 
                                                    hx-trigger="click"
                                                    class="btn btn-primary btn-block"
                                                    _="on htmx:afterOnLoad wait 10ms then add .show to #modal then add .show to #modal-backdrop">Сохранить11
                                                </button>
                                            </td>                                            
                                            <td style="text-align: right;"> 
                                                <button type="button" class="btn btn-danger" onclick="closeModal1()">&nbsp;Отмена&nbsp;</button>
                                            </td>                                            
                                        </tr>
                                    </table>    
                                </div>
                            </div>
                            </div>
                        </div>"""
        return response

# Модальное на закрытие---------------------------------------------------------------------------------------------------------------------------------
@zakaz_naryad.route('/zn_modal_close_btn', methods=['GET', 'POST'])
def zn_modal_close_btn():
        
    if request.method == 'POST':
        idkv = request.args.get('idkv')
        dt_close = request.args.get('dt_close')
        return redirect(url_for('zakaz_naryad.zn_modal_close_btn', idkv=idkv, dt_close=dt_close))
    else:
        idkv = request.args.get('idkv')
        dt_close = request.args.get('dt_close')
        response = f"""{idkv} {dt_close} """
        return response, "12312"
    