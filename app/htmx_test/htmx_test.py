""" gh"""
from operator import mod
from pydoc import doc
from re import M
from flask import Flask, render_template, redirect, url_for, request, Blueprint, session
from loguru import logger
import json
import os.path
import app.db as db
import app.sql as sql
from app.data_input.sql_data_input import sql_upd_it_rasp_grf, sql_upd_it_rasp_grf_, SQL_DELETE_GRF
from dateutil import parser
from datetime import date
import calendar
import app.utils as utils

data = ["Один", "Тор"]

htmx_test = Blueprint('htmx_test', __name__)


@htmx_test.route("/name/create", methods=["POST"])
@logger.catch
def name_create():
    """_summary_

    Returns:
        response: any
    """    
    name = request.form["create"]
    data.append(name)
    vals = json.dumps({"delete": name})
    response = f"""
    <tr>
        <td><input readonly type="text" name='{name}' value='{name}'></td>
        <td><span id='clickableAwesomeFont'><i class='fas fa-trash fa-lg' name='{{name}}' hx-post='name/delete' hx-vals='{vals}' hx-target='closest tr' hx-swap='outerHTML swap:0.5s'></i></span></td>
        <td><i class='fas fa-ellipsis-v'></i></td>
    </tr>
    """
    return response


@htmx_test.route("/name/delete", methods=["POST"])
@logger.catch
def name_delete():
    name = request.form["delete"]
    print(f"{name} removed")
    data.remove(name)
    return ""


@htmx_test.route("/name/order", methods=["POST"])
@logger.catch
def name_order():
    global data
    order = request.form.keys()
    data = list(order)
    print(data)
    return f"Stages reordered - "


@htmx_test.route("/")
@logger.catch
def index():
    menu = session['menu']
    return render_template("htmx_test.html", items=data, menu=menu)

def create_th(cur_year,cur_month):
    """функция формирования заголовка таблицы

    Args:
        cur_year (_type_): string  год
        cur_month (_type_): string месяц 

    Returns:
        _type_: dict словарь с номерами дней месяца
    """   
    all_day = calendar.monthrange(int(cur_year), int(cur_month))[1]
    result_th_ = {}
    for i in range(all_day):
        i+=1
        current_data = f'{str(i)}.{str(cur_month)}.{str(cur_year)}'
        color_day_week = utils.date_color(current_data)
        current_data_ =  f'{str(cur_month)}.{str(i)}.{str(cur_year)}'
        russian_dayWeek = utils.russianNameDayWeek(current_data_)
        if i<10 :
            p=f'0{i}'
        else:
            p=str(i) 
        value_ = f"""{p}  {russian_dayWeek}"""
        key_ = f'day{str(i)}'
        result_th_[key_] = [color_day_week,value_]
    return result_th_


@htmx_test.route("/table_view", methods=["GET", "POST"])
@logger.catch
def table_view():
    """отображение таблицы с расписанием, ничего интересного
    Returns:
        html страницу (htmx_tableview.html) с таблицей, смотреть внимательно
    """
    if 'arena_user' in session:
        arena_user = session.get('arena_user')
    else:
        arena_user = 0
    select_otd = utils.access_user_otd(arena_user)  #доступные отделения
    select_sdl = utils.access_user_sdl(arena_user)  #доступные должности
    current_date = date.today()                     #текущая дата
    current_year = parser.parse(current_date.strftime('%m/%d/%y')).strftime("%Y")  #текущий год
    current_month = parser.parse(current_date.strftime('%m/%d/%y')).strftime("%m") #текущий месяц
    all_month = {}
    all_month['01'] = 'Январь'
    all_month['02'] = 'Февраль'
    all_month['03'] = 'Март'
    all_month['04'] = 'Апрель'
    all_month['05'] = 'Май'
    all_month['06'] = 'Июнь'
    all_month['07'] = 'Июль'
    all_month['08'] = 'Август'
    all_month['09'] = 'Сентябрь'
    all_month['10'] = 'Октябрь'
    all_month['11'] = 'Ноябрь'
    all_month['12'] = 'Декабрь'  
    nmonth = all_month[str(current_month)]
    # del all_month[str(current_month)]
    
    last_day = calendar.monthrange(int(current_year), int(current_month))[1]
    result_otd = db.select(sql.SQL_ALLOTD.format(select_otd=select_otd)) #список отделений доступных пользователю
    otd = request.args.get('otd') or result_otd[0][0] #первое в списке или выбранное отделение
    notd = db.select(sql.sql_currentOtd.format(otd=otd))[0][1] #наименование выбранного отделения
    current_otd = f' and otd={otd}'
    
    result_th = {}  #список для построения заголовка таблицы
    result_th = create_th(current_year,current_month).copy()         
      
    result_alldoc = db.select(sql.sql_allDoc.format(current_otd=current_otd, select_sdl = select_sdl)) #список врачей
    result_time = db.select(sql.sql_interval_time) #интервал времени
    
    if request.method == 'POST':
        if request.form['btn'] == 'selectNew':
            otd=request.form.get('otd')
            notd = db.select(sql.sql_currentOtd.format(otd=otd))[0][1]
            current_otd = f' and otd={otd}'
            current_year=request.form.get('year')
            current_month=request.form.get('month')
            last_day = calendar.monthrange(int(current_year), int(current_month))[1]
            # all_month[current_month] = nmonth
            
            nmonth = all_month[str(current_month)]
            # del all_month[str(current_month)] 
    
            result_th = {}
            result_th = create_th(current_year,current_month).copy()
            result_alldoc = db.select(sql.sql_allDoc.format(current_otd=current_otd, select_sdl = select_sdl)) #список врачей 
            
        if request.form['btn'] == 'sotrudnikNew':
            otd=request.form.get('otd')
            notd = db.select(sql.sql_currentOtd.format(otd=otd))[0][1]
            current_year=request.form.get('year')
            current_month=request.form.get('month')
            result_alldoc = db.select(sql.sql_allDoc.format(otd=otd, select_sdl = select_sdl)) #список врачей
            
    sel_dop_day='';
    visible_29 = ''
    visible_30 = ''
    visible_31 = ''

    if last_day==28:
        visible_29 = 'style=display:none;'
        visible_30 = 'style=display:none;'
        visible_31 = 'style=display:none;'

    if last_day==29:
        sel_dop_day = """,(select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29 """ 
        visible_30 = 'style=display:none;'
        visible_31 = 'style=display:none;'

    if last_day==30:
        sel_dop_day = """,(select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day30) as day30 """ 
        visible_31 = 'style=display:none;'
                
    if last_day==31:
        sel_dop_day = """,(select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day30) as day30,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day31) as day31 """ 
     
    menu = session['menu']
    table_view_all = db.select_dicts_in_turple(sql.sql_TabelWorkTime.format(otd=otd, EYear=current_year, EMonth=current_month, sel_dop_day=sel_dop_day)) 
    return render_template("htmx_tableview.html", 
                           table_view_all = table_view_all,
                           result_th = result_th,
                           result_otd=result_otd,
                           year = current_year,
                           month = current_month,
                           nmonth = nmonth,
                           all_month = all_month,
                           notd = notd,
                           otd = otd,
                           menu = menu,
                           result_alldoc = result_alldoc,
                           visible_29 = visible_29,        
                           visible_30 = visible_30,
                           visible_31 = visible_31)


@htmx_test.route("/table_view/edit", methods=["GET", "POST"])
@logger.catch
def table_edit():
    #TODO:  1. Переименовать нормально переменные
    #       2. В блоке POST переменной rasp_id возвращается код в базе а не значение, 
    #     нужно выбрать из базы и передать в html шаблон значение времени
    #       3. Подумать над вводом произвольного времени
    """Функция для редактирования данных таблицы

    Returns:
        GET  - Выбираем из БД список расписаний,
            формируем html form для замены оригинального блока и возвращаем на страницу
        POST - Записываем выбранное значение из выпадающего списка в БД,
            Заполняем нужными данными для последующего редактирования
            и новыми выбранными данными html и возвращаем обратно на страницу
    """
    if request.method == 'POST':
        id_td = request.args.get('id_td')
        s_id_td = id_td[2:4]
        s_id_td = f'day{s_id_td}'    
        id_grf = request.args.get('id_grf')
        rasp_id = request.form.get('rasp_id')
        rasp_id_visible =db.select( sql.sql_interval_time_current.format(id=rasp_id))
        rasp_id_visible = rasp_id_visible[0][0]
        
        db.write(sql_upd_it_rasp_grf.format(day_col=s_id_td, day_zn=rasp_id, id_grf=id_grf))
        
        response = f"""
            <div name="id_grf" 
                hx-target="#{id_td}" 
                hx-swap="innerHTML" hx-get="table_view/edit?id_td={id_td}&id_grf={id_grf}">{rasp_id_visible}
            </div>
        """
        return response
    else:
        id_td = request.args.get('id_td')
        id_grf = request.args.get('id_grf')
        list_of_time = db.select(sql.sql_interval_time)
        list_of_options = ''
        i = 1
        while i < (len(list_of_time)):
            option = f"""<option value="{list_of_time[i][0]}">{list_of_time[i][1]}</option>"""
            list_of_options = list_of_options + option
            i += 1
        response = f"""
                <div>
                    <select name="rasp_id" hx-post="table_view/edit?id_grf={id_grf}&id_td={id_td}" 
                        hx-target="#{id_td}" hx-swap="innerHTML" hx-indicator=".htmx-indicator">
                        {list_of_options}
                    </select>
                </div>
            """
        return response
    
@htmx_test.route('/grf_NewWork', methods=['GET', 'POST'])
@logger.catch
def NewWork():
    otd = request.args.get('otd')
    y = request.args.get('year') #год
    m = request.args.get('month') #месяц
    response = f"""<button
                    hx-get="grf_addWorker?otd={otd}&year={y}&month={m}" 
                    hx-target="#modals-here" 
                    hx-trigger="click"
                    class="btn btn-primary btn-block">Добавить сотрудника</button>
                    </div>"""
    return response

@htmx_test.route('/grf_deleteRowTableModal', methods=['GET', 'POST'])
@logger.catch
def delete_rowtablemodal(): 
    """вызов модального окна для удаления сотрудника из таблицы график работы

    Returns:
        _type_: _description_
    """          
    otd = request.args.get('otd')
    year = request.args.get('year') #год
    month = request.args.get('month') #месяц 
    idz = request.args.get('idz') #ун.код записи   
    response = f"""<div id="modal-backdrop_del_work" class="modal-backdrop fade show" style="display:block;"></div>
                        <div id="modal_delete_work" class="modal fade show" tabindex="-1" style="display:block;">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <div class="row" style="text-align: center;">
                                                <div class="col mx-auto">
                                                    <h5 class="modal-title">Вы действительно хотите удалить сотрудника из графика?</h5>
                                                </div>
                                            </div>
                                        </div>
                                        <form hx-post="grf_deleteRowTableGrf?idz={idz}&otd={otd}&year={year}&month={month}" 
                                              hx-select="#myTable"
                                              hx-swap="outerHTML"
                                              hx-target="#myTable">
                                            <div class="modal-footer">
                                                <div class="container-fluid">
                                                    <div class="row">
                                                        <div class="col-md-4">
                                                            <button class="btn btn-primary btn-block btn-success" type="submit" onclick="closeModal_DelRow()">Да</button>
                                                        </div>
                                                        <div class="col-md-4">
                                                        </div>
                                                        <div class="col-md-4">
                                                            <button type="button" class="btn btn-danger btn-block" onclick="closeModal_DelRow()">Нет</button>
                                                        </div>
                                                    </div>
                                                </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """
    return response

@htmx_test.route('/grf_deleteRowTableGrf', methods=['POST'])
@logger.catch
def delete_rowtablegrf():
    """удаление из таблицы (график работы) сотрудника
    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        idz = request.args.get('idz')
        otd = request.args.get('otd') #код отделения
        lpu = int(db.select(sql.sql_currentOtd.format(otd=otd))[0][2])
        cur_year = request.args.get('year') #год
        cur_month = request.args.get('month') #месяц
        db.write(SQL_DELETE_GRF.format(id_grf=idz))
        return redirect(url_for("htmx_test.table_view", otd=otd, year=cur_year, month=cur_month))

@htmx_test.route('/grf_addWorker', methods=['GET', 'POST'])
@logger.catch
def modal_addworker():
    """Добавление сотрудника в график работы

    Returns:
        _type_: _description_
    """       
    if 'arena_user' in session:
        arena_user = session.get('arena_user')
    else:
        arena_user = 0
            
    if 'arena_mpp' in session:
        arena_mpp = session.get('arena_mpp')
    else:
        arena_mpp = 0
        
    select_sdl = utils.access_user_sdl(arena_user = arena_user)
    otd = request.args.get('otd')
    y = request.args.get('year') #год
    m = request.args.get('month') #месяц
    current_otd=f' and otd={ otd }'
    result_alldoc = db.select(sql.sql_allDoc.format(current_otd=current_otd,select_sdl=select_sdl)) #список врачей
    result_time = db.select(sql.sql_interval_time) #интервал времени
    sql_room = db.select(sql.sql_room_mpp.format(mpp = arena_mpp)) #кабинеты

    sel_doc = ['<option value="0">Не назначен</option>', ] 
    for i in range(1, len(result_alldoc)):
        sel_vol = f"""<option value="{result_alldoc[i][0]}">{result_alldoc[i][1]}</option>"""
        sel_doc.append(sel_vol)

    sel_room = ['<option value="0">Не назначен</option>', ] 
    for i in range(1, len(sql_room)):
        sel1_vol = f"""<option value="{sql_room[i][0]}">{sql_room[i][1]}</option>"""
        sel_room.append(sel1_vol)
        
    sel_noeven = ['<option value="0">Не назначен</option>', ] 
    for i in range(1, len(result_time)):
        sel2_vol = f"""<option value="{result_time[i][0]}">{result_time[i][1]}</option>"""
        sel_noeven.append(sel2_vol)
        
    sel_even = ['<option value="0">Не назначен</option>', ] 
    for i in range(1, len(result_time)):
        sel2_vol = f"""<option value="{result_time[i][0]}">{result_time[i][1]}</option>"""
        sel_even.append(sel2_vol)
        
                                        
    response = f"""<!--html--> <div id="modal-backdrop" class="modal-backdrop fade show" style="display:block;"></div>
                        <div id="modal" class="modal fade show" tabindex="-1" style="display:block;">
                            <div class="modal-dialog modal-dialog-centered modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title">Добавить сотрудника</h5>
                                        
                                    </div>
                                    
                                    <form hx-post="grf_insWorkerTable?otd={otd}&year={y}&month={m}"> 
                                        <div class="modal-body">                                        
                                            <div class="input-group mb-3">
                                                <label class="col-form-label input-group-text" for="worker_select" style = "width:188px;">Сотрудник</label> 
                                                <select class="custom-select form-control" id="worker_select"  name = "worker_select">                                                
                                                    {sel_doc}
                                                </select>
                                            </div>
                                                                               
                                            <div class="input-group mb-3">
                                                <label class="custom-select-label input-group-text" for="room_select" style = "width:188px;">№ кабинета</label> 
                                                <select class="custom-select" id="room_select"  name = "room_select">                                                
                                                    {sel_room}
                                                </select>
                                            </div>
                                                
                                            <div class="input-group mb-3">
                                                <label class="col-form-label input-group-text">Норма часов в месяц:</label>
                                                <input type="number" class="form-control" name="UpdNclock">
                                            </div>    
                                                
                                            <div class="input-group mb-3">
                                                <label class="custom-select-label input-group-text" for="noeven_select" style = "width:188px;">Не четное</label> 
                                                <select class="custom-select" id="noeven_select"  name = "noeven_select">                                                
                                                    {sel_noeven}
                                                </select>
                                            </div>
                                                
                                            <div class="input-group mb-3">
                                                <label class="custom-select-label input-group-text" for="even_select" style = "width:188px;">Четное</label> 
                                                <select class="custom-select" id="even_select"  name = "even_select">                                                
                                                    {sel_even}
                                                </select>
                                            </div>                                                                          
                                        </div>
                        
                                        <div class="modal-footer">
                                           <table class="table table-borderless">
                                                <tr>
                                                    <td style="text-align: left;">
                                                        <button class="btn btn-primary btn-success" type="submit" style = "width:185px;" onclick="closeModal()">Сохранить</button>  
                                                    </td>                                            
                                                    <td style="text-align: right;"> 
                                                        <button class="btn btn-danger" type="button" style = "width:185px;" onclick="closeModal()">&nbsp;Отмена&nbsp;</button> 
                                                    </td>                                            
                                                </tr>
                                           </table>     
                                        </div>                                
                                    </form>  
                                </div>
                            </div>
                        </div>   
                     <!--!html-->"""
    return response


@htmx_test.route('/grf_insWorkerTable', methods=['GET', 'POST'])
@logger.catch
def grf_insWorkerTable():
    #добавить новую запись в таблицу IT_RASP_GRF
    procedure_name = 'NEW_GEN_IT_RASP_GRF_ID'
    output_params = db.proc(procedure_name)[0]
    otd = request.args.get('otd') #код отделения
    lpu = int(db.select(sql.sql_currentOtd.format(otd=otd))[0][2])
    cur_year = request.args.get('year') #год
    cur_month = request.args.get('month') #месяц       
    nclock = request.form.get('UpdNclock') #норма часов
    doc = request.form.get('worker_select') #код сотрудника
    spz = db.select(sql.sql_doctod.format(otd=otd, doc=doc))[0][2] 
    room = request.form.get('room_select') #номер кабинета
    new_data = f' LPU={lpu}, OTD={otd}, SPZ={spz}, DOC={doc}, YEARWORK={cur_year}, MONTHWORK={cur_month}, NCLOCK={nclock}, ROOM={room} '
    #обновить данные с учетом введенного режима работы и отсутствия на работе
    result_it_rasp = db.select(sql.sql_it_rasp.format(doc=doc))
    noeven_day = request.form.get('noeven_select') or result_it_rasp[0][2] 
    even_day = request.form.get('even_select') or result_it_rasp[0][4]
    all_day = calendar.monthrange(int(cur_year), int(cur_month))[1] 
    for i in range(all_day):
        i+=1
        if i<10 :
           p=f'0{i}'
        else:
           p=str(i)  
    nf = f'day{p}'  #название колонки day01 .. day31
    current_data = f'{p}.{str(cur_month)}.{str(cur_year)}'
    select_period = f''' and (dtn>='{current_data}' and dtk<='{current_data}')'''
    result_rsp_blc=db.select(sql.sql_noWork.format(doc=doc,period=select_period))    
    if result_rsp_blc == []:
        if (i % 2) ==0: 
            new_data = f'{new_data},{nf}={even_day}'
        else:   
            new_data = f'{new_data},{nf}={noeven_day}'       
    db.write(sql_upd_it_rasp_grf_.format(new_data=new_data, id_grf=output_params))
    return redirect(url_for("htmx_test.table_view", otd=otd, year=cur_year, month=cur_month))
    
