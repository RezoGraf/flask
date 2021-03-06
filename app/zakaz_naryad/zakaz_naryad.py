import app.db as db
import app.sql as sql
import app.api.api as api
from flask import render_template, request, url_for, redirect, Blueprint
from datetime import datetime
from app.menu_script import generate_menu
import re
from loguru import logger

zakaz_naryad = Blueprint('zakaz_naryad', __name__)

url_back = ""

@zakaz_naryad.route('/', methods=['GET', 'POST'])
def main():
    """_summary_

    Returns:
        _type_: _description_
    """
    menu = generate_menu()
    global url_back
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
            url_back = request.url
            return render_template("zakaz_naryad.html", my_list=result, menu=menu, dtn_get=dtn_simple,
                                   dtk_get=dtk_simple, check1=check_open, check2=check_close)
        if check_open is None and check_close:
            # print('close')
            result = db.select(sql.sql_zakaz_naryad_select_close.format(dtn=dtn, dtk=dtk))
            url_back = request.url
            return render_template("zakaz_naryad.html",
                            my_list=result, menu=menu, dtn_get=dtn_simple, dtk_get=dtk_simple, check1=check_open, check2=check_close)
        if check_open and check_close is None:
            # print('open')
            result = db.select(sql.sql_zakaz_naryad_select_open.format(dtn=dtn, dtk=dtk))
            url_back = request.url
            return render_template("zakaz_naryad.html",
                            my_list=result, menu=menu, dtn_get=dtn_simple, dtk_get=dtk_simple, check1=check_open, check2=check_close)
        else:
            # print('default')
            menu = generate_menu()
            result = db.select(sql.sql_zakaz_naryad_select.format(dtn=dtn, dtk=dtk))
            url_back = request.url
            return render_template("zakaz_naryad.html",
                                menu = menu,
                                my_list=result,
                                dtn_get=dtn_simple,
                                dtk_get=dtk_simple,
                                check1='checked',
                                check2='')
#Наряд------------------------------------------------
@zakaz_naryad.route('/zn_naryad', methods=['GET', 'POST'])
def zn_naryad():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        idkv = request.form.get('idkv')
        return redirect(url_for('zakaz_naryad.zn_naryad', idkv=idkv))
    else:
        ub = url_back
        idkv = request.args.get('idkv')
        result = db.select(sql.sql_zn_naryad_select_info.format(idkv=idkv))
        result_usl = db.select(sql.sql_zn_naryad_select_usl.format(idkv=idkv))
        menu = generate_menu()     
        return render_template('zn_naryad.html', menu=menu, ub=ub,
                               result_usl = result_usl,
                               zn_naryad_list=result,
                               idkv=idkv)
#Модальное на редактирование наряда---------------------------
@zakaz_naryad.route('/zn_modal_edit', methods=['GET', 'POST'])
def zn_modal_edit():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        idkv = request.args.get('idkv')
        nom_teh = request.args.get("nom_teh")
        nom_lit = request.args.get("nom_lit")
        nom_pol = request.args.get("nom_pol")
        nom_var = request.args.get("nom_var")
        dzr = request.args.get("dzr")
        result = db.select(sql.sql_zn_naryad_select_info.format(idkv=idkv))
        return redirect(url_for('zakaz_naryad.zn_modal_edit', zn_naryad_list=result, idkv=idkv,
                                nom_teh=nom_teh, nom_lit=nom_lit, nom_pol=nom_pol, nom_var=nom_var))
    else:
        idkv = request.args.get('idkv')
        nom_teh = request.args.get("nom_teh")
        nom_lit = request.args.get("nom_lit")
        nom_pol = request.args.get("nom_pol")
        nom_var = request.args.get("nom_var")
        dzr = request.args.get("dzr")
        result = db.select(sql.sql_zn_naryad_select_info.format(idkv=idkv))
        nteh_db = db.select(sql.sql_zn_naryad_select_teh)
        nlit_db = db.select(sql.sql_zn_naryad_select_lit)
        npol_db = db.select(sql.sql_zn_naryad_select_pol)
        nvar_db = db.select(sql.sql_zn_naryad_select_var)
# Построение выпадающего списка-------------------------------------------------
        sel_1 = ['<option value="0">Не назначен</option>', ]
        for i in range(1, len(nteh_db)):
            sel_1_vol = f"""<option value="{nteh_db[i][0]}">{nteh_db[i][1]}</option>"""
            # print(nteh_db[i][0])
            sel_1.append(sel_1_vol)
        # print(sel_1)
        for i in range(1, len(sel_1)):
            if str('"'+nom_teh+'"') in sel_1[i]:
                # print(nom_teh)
                sel_1[i] = f"""<option value="{nom_teh}" selected>{nteh_db[i][1]}</option>"""
                # print(sel_1[i])
        sel_2 = ['<option value="0">Не назначен</option>', ]
        for i in range(1, len(nlit_db)):
            sel_2_vol = f"""<option value="{nlit_db[i][0]}">{nlit_db[i][1]}</option>"""
            sel_2.append(sel_2_vol)
        for i in range(1, len(sel_2)):
            if str('"'+nom_lit+'"') in sel_2[i]:
                sel_2[i] = f"""<option value="{nom_lit}" selected>{nlit_db[i][1]}</option>"""
        sel_3 = ['<option value="0">Не назначен</option>', ]
        for i in range(1, len(npol_db)):
            sel_3_vol = f"""<option value="{npol_db[i][0]}">{npol_db[i][1]}</option>"""
            sel_3.append(sel_3_vol)
        for i in range(1, len(sel_3)):
            if str('"'+nom_pol+'"') in sel_3[i]:
                sel_3[i] = f"""<option value="{nom_pol}" selected>{npol_db[i][1]}</option>"""
        sel_4 = ['<option value="0">Не назначен</option>', ]
        for i in range(1, len(nvar_db)):
            sel_4_vol = f"""<option value="{nvar_db[i][0]}">{nvar_db[i][1]}</option>"""
            sel_4.append(sel_4_vol)
        for i in range(1, len(sel_4)):
            if str('"'+nom_var+'"') in sel_4[i]:
                sel_4[i] = f"""<option value="{nom_var}" selected>{nvar_db[i][1]}</option>"""
        response = f"""<div id="modal-backdrop" class="modal-backdrop fade show" style="display:block;"></div>
                        <div id="modal" class="modal fade show" tabindex="-1" style="display:block;">
                            <div class="modal-dialog modal-dialog-centered modal-lg">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <div class="row" style="text-align: center;">
                                        <div class="col mx-auto">
                                            <h5 class="modal-title" >Наряд № {result[0][1]}</h5>
                                        </div>
                                    </div>                                
                                </div>
                                <form hx-post="zn_modal_close_btn?idkv={idkv}">
                                <div class="modal-body">
                                        
                                        <table class="table table-borderless">
                                            <tr>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="nom_teh">Зубной техник</label> 
                                                    <select class="custom-select" id="nom_teh" name="nom_teh">                                                
                                                        {sel_1}
                                                    </select>
                                                </td>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="nom_lit">Литейщик</label>
                                                    <select class="custom-select" id="nom_lit" name="nom_lit">                                                
                                                        {sel_2}
                                                    </select>
                                                </td>
                                            </tr>
                                            <tr>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="nom_pol">Полировщик</label>
                                                    <select class="custom-select" id="nom_pol" name="nom_pol">
                                                        {sel_3}
                                                    </select>
                                                </td>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="nom_var">Варщик</label>
                                                    <select class="custom-select" id="nom_var" name="nom_var">
                                                        {sel_4}
                                                    </select>
                                                </td>
                                            </tr>
                                                    
                                        </table>
                                        <div class="row">
                                            <div class="mx-auto">
                                                <input type="date" value="{dzr}" name="dzr" id="dzr" />
                                            </div>
                                        </div>
                                </div>
                                <div class="modal-footer">
                                    <table class="table table-borderless">
                                        <tr>
                                            <td style="text-align: left;">
                                            <button class="btn btn-primary btn-success" type="submit" onclick="closeModal()">Сохранить</button>
                                            </td>                                            
                                            <td style="text-align: right;"> 
                                                <button type="button" class="btn btn-danger" onclick="closeModal1()">&nbsp;Отмена&nbsp;</button>
                                                
                                            </td>                                            
                                        </tr>
                                </div>
                            </div>
                            </div>
                        </div>
                        </form>  """
        return response
    
# Модальное на закрытие---------------------------------------------------------
@zakaz_naryad.route('/zn_modal_close_btn', methods=['GET', 'POST'])
@logger.catch
def zn_modal_close_btn():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        idkv = request.args.get('idkv')
        dzr = request.form.get('dzr')
        nom_teh = request.form.get('nom_teh')
        nom_lit = request.form.get('nom_lit')
        nom_pol = request.form.get('nom_pol')
        nom_var = request.form.get('nom_var')
        return redirect(url_for('zakaz_naryad.zn_modal_close_btn', idkv=idkv, dzr=dzr, nom_teh=nom_teh, nom_lit=nom_lit, nom_pol=nom_pol, nom_var=nom_var))
    else:
        idkv = request.args.get('idkv')
        dzr = request.args.get('dzr')
        nom_teh = request.args.get('nom_teh')
        nom_lit = request.args.get('nom_lit')
        nom_pol = request.args.get('nom_pol')
        nom_var = request.form.get('nom_var')
        if nom_teh is None:
            nom_teh = "0"
        if nom_lit is None:
            nom_lit = "0"
        if nom_pol is None:
            nom_pol = "0"
        if nom_var is None:
            nom_var = "0"
        check_dzr = 0
        if re.fullmatch(r"\d{4}-\d\d-\d\d", dzr):
            date_time_obj = datetime.strptime(dzr, '%Y-%m-%d')
            dzr = date_time_obj.strftime('%d.%m.%Y')
            dzr = f"'{dzr}'"
            check_dzr = 2
        if dzr is None or dzr == "" or dzr == " ":
            dzr = "null"
            check_dzr = 1
# Проверка даты----------------------------------------------------------------------------------
        if check_dzr == 1 or 2:
            check_zn = db.select(sql.sql_zn_naryad_select_info_isp.format(idkv=idkv))
            if check_zn == []:
                db.write(sql.sql_zn_naryad_insert_isp.format(idkv=idkv, nom_teh=nom_teh, nom_lit=nom_lit, nom_pol=nom_pol, nom_var=nom_var, dzr=dzr))
                # если дата формата дд.мм.гг то запись на отправку---------------------------------
                if check_dzr == 2:
                    db.write(sql.sql_zn_naryad_update_uslk.format(idkv=idkv, status=3, dzr=dzr))
                    api.zn_close()
                return redirect(url_for('zakaz_naryad.zn_naryad', idkv=idkv))
            else:
                db.write(sql.sql_zn_naryad_update_isp.format(idkv=idkv, nom_teh=nom_teh, nom_lit=nom_lit, nom_pol=nom_pol, nom_var=nom_var, dzr=dzr))
                if check_dzr == 2:
                    db.write(sql.sql_zn_naryad_update_uslk.format(idkv=idkv, status=3, dzr=dzr))
                    api.zn_close()
        return redirect(url_for('zakaz_naryad.zn_naryad', idkv=idkv))

# Кнопка удаления даты закрытия наряда--------------------------------------------------------------
@zakaz_naryad.route('/zn_modal_open_btn', methods=['GET', 'POST'])
def zn_modal_open_btn():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        idkv = request.args.get('idkv')
        nkv = request.args.get('nkv')
        return redirect(url_for('zakaz_naryad.zn_modal_open_btn', idkv=idkv, nkv=nkv))
    else:
        idkv = request.args.get('idkv')
        nkv = request.args.get('nkv')
        response = f"""<!--html--><div id="modal-backdrop_zn_open" class="modal-backdrop fade show" style="display:block;"></div>
                        <div id="modal_zn_modal" class="modal fade show" tabindex="-1" style="display:block;">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <div class="row" style="text-align: center;">
                                                <div class="col mx-auto">
                                                    <h5 class="modal-title" >Вы действительно хотите удалить дату закрытия наряд № {nkv}?</h5>
                                                </div>
                                            </div>                             
                                        </div>
                                        <form hx-post="zn_modal_open?idkv={idkv}">                               
                                            <div class="modal-footer">
                                                <div class="container-fluid">
                                                    <div class="row">
                                                        <div class="col-md-4">
                                                            <button class="btn btn-primary btn-block btn-success " type="submit" onclick="closeModal_zn_open()">Да</button>
                                                        </div>
                                                        <div class="col-md-4">
                                                        </div>
                                                        <div class="col-md-4">
                                                            <button type="button" class="btn btn-danger btn-block" onclick="closeModal_zn_open_close()">Нет</button>  
                                                        </div>
                                                    </div>
                                                </div>                                       
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                          <!--!html-->"""
        return response

@zakaz_naryad.route('/zn_modal_open', methods=['GET', 'POST'])
def zn_modal_open():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        idkv = request.args.get('idkv')
        return redirect(url_for('zakaz_naryad.zn_modal_open', idkv=idkv))
    else:
        idkv = request.args.get('idkv')
        db.write(sql.sql_zn_naryad_update_dzr_uslk.format(idkv=idkv))
        db.write(sql.sql_zn_naryad_update_dzr_uslt.format(idkv=idkv))
    return redirect(url_for('zakaz_naryad.zn_naryad', idkv=idkv))

@zakaz_naryad.route('/zn_modal_fullwin_btn', methods=['GET', 'POST'])
@logger.catch
def zn_modal_fullwin_btn():
    """_summary_

    Returns:
        _type_: _description_
    """
    idkv = request.args.get('idkv')
    nkv = request.args.get('nkv')
    all_sris = db.select(sql.sql_zn_naryad_sel_sris)
    sel_sris = '<option disabled selected>Выберити тип рыбот</option>'
    print(all_sris)
    for i, _ in enumerate(all_sris):
        sel_sris_vol = f"""<option value="{all_sris[i][0]}">{all_sris[i][1]}</option>"""
        sel_sris = sel_sris + sel_sris_vol
    response = f"""<!--html-->
        <div id="fullscreen_modal_workers" class="modal fade modal-fullscreen show" style="display:block">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Наряд № {nkv}</h5>
                        <button type="button" class="close" _="on click remove #fullscreen_modal_workers" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <form>
                    <div class="modal-body">
                        <div class="container-fluid">
                            <div class="row">
                                <div class="col-md-12">
                                    <select select class="custom-select" name="sris_id" hx-post="zn_modal_fullwin_tab1" hx-target="#models" hx-indicator=".htmx-indicator">
                                        {sel_sris}
                                    </select>
                                    <hr/>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div id="models"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" _="on click remove #fullscreen_modal_workers" class="btn btn-secondary">Close</button>
                        <button type="button" class="btn btn-primary">Save changes</button>
                    </div>
                    </form>
                </div>
            </div>
        </div>
        <!--!html-->"""
    return response

@zakaz_naryad.route('/zn_modal_fullwin_tab1', methods=['GET', 'POST'])
@logger.catch
def zn_modal_fullwin_tab1():
    """_summary_

    Returns:
        _type_: _description_
    """
    sris_id = request.form.get('sris_id')
    all_stage = db.select(sql.sql_zn_naryad_sel_stage.format(sris_id=sris_id))
    sel_stage = ''
    for i, _ in enumerate(all_stage):
        sel_stage_vol = f"""<div class="form-check" onmouseover="this.style.backgroundColor='#BADAFF';" onmouseout="this.style.backgroundColor='#fff';">
                                <input class="form-check-input" type="checkbox" value="{all_stage[i][0]}" id="chek_stage{i}" checked>
                                <label class="form-check-label" for="chek_stage{i}">{all_stage[i][2]}</label>
                            </div><hr/>"""
        sel_stage = sel_stage + sel_stage_vol
    response = f"""{sel_stage}"""
    return response