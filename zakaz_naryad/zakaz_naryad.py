import db, sql
from api.api import api
from data_input.data_input import data_input
from flask import Flask, render_template, request, url_for, redirect, Blueprint
# регистрируем схему `Blueprint`
from data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc
from data_input.sql_data_input import sql_ins_rsp_blc, sql_ins_it_rasp_duty
from . import zakaz_naryad
import pandas as pd
from datetime import datetime
import calendar


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
    