from pydoc import doc
from flask import Flask, render_template, redirect, url_for, request, Blueprint, session
import json
import os.path
import app.db as db
import app.sql as sql
from app.data_input.sql_data_input import sql_upd_it_rasp_grf, sql_upd_it_rasp_grf_
from dateutil import parser
from datetime import date
import calendar
import app.utils as utils
from app.menu_script import generate_menu


data = ["Один", "Тор"]

htmx_test = Blueprint('htmx_test', __name__)

            
@htmx_test.route("/name/create", methods=["POST"])
def name_create():
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
def name_delete():
    name = request.form["delete"]
    print(f"{name} removed")
    data.remove(name)
    return ""


@htmx_test.route("/name/order", methods=["POST"])
def name_order():
    global data
    order = request.form.keys()
    data = list(order)
    print(data)
    return f"Stages reordered - "


@htmx_test.route("/")
def index():
  menu = generate_menu()
  return render_template("htmx_test.html", items=data, menu=menu)

# функция формирования заголовка таблицы
def create_th(cur_year,cur_month):
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
    last_day = calendar.monthrange(int(current_year), int(current_month))[1]
    result_otd = db.select(sql.sql_allOtd.format(select_otd=select_otd))           #список отделений доступных пользователю
    otd = request.form.get('otd') or result_otd[0][0] #первое в списке или выбранное отделение
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
    if last_day==29:
        sel_dop_day = """,(select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29 """ 
    if last_day==30:
        sel_dop_day = """,(select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day30) as day30 """ 
    if last_day==31:
        sel_dop_day = """,(select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day30) as day30,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day31) as day31 """ 
     
    menu = generate_menu
    print(sql.sql_TabelWorkTime.format(otd=otd, EYear=current_year, EMonth=current_month, sel_dop_day=sel_dop_day))
    table_view_all = db.select_dicts_in_turple(sql.sql_TabelWorkTime.format(otd=otd, EYear=current_year, EMonth=current_month, sel_dop_day=sel_dop_day)) 
    return render_template("htmx_tableview.html", 
                           table_view_all = table_view_all,
                           result_th = result_th,
                           result_otd=result_otd,
                           year = current_year,
                           month = current_month,
                           notd = notd,
                           otd = otd,
                           menu = menu,
                           result_alldoc = result_alldoc)


@htmx_test.route("/table_view/edit", methods=["GET", "POST"])
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
def NewWork():
    otd = request.args.get('otd')
    y = request.args.get('year') #год
    m = request.args.get('month') #месяц   
    response = f"""
     <button 
      hx-get="grf_addWorker?otd={otd}&year={y}&month={m}" 
      hx-target="#modals-here" 
      hx-trigger="click"
      class="btn btn-primary btn-block" >Добавить сотрудника</button>
      </div>"""
    return response
    
    
#Модальное на добавление сотрудника в график работы-------------------------------------------------------------------------------------------- 
@htmx_test.route('/grf_addWorker', methods=['GET', 'POST'])
def modal_addWorker():
        
    if request.method == 'POST':
        #добавить новую запись в таблицу IT_RASP_GRF
        # procedure_name = 'NEW_GEN_IT_RASP_GRF_ID'
        # output_params = db.proc(procedure_name)[0][0]
        #  output_params = utils.list_to_int(output_params)  
        # doc = request.args.get('doc') #код сотрудника
        # db.write(sql_upd_it_rasp_grf_.format(day_col=s_id_td, day_zn=rasp_id, id_grf=output_params))
        id_td = request.args.get('id_td')
        s_id_td = id_td[2:4]
        s_id_td = f'day{s_id_td}'    
        id_grf = request.args.get('id_grf')
        rasp_id = request.form.get('rasp_id')
        rasp_id_visible =db.select( sql.sql_interval_time_current.format(id=rasp_id))
        rasp_id_visible = rasp_id_visible[0][0] 
        response = f"""
            <div name="id_grf" 
                hx-target="#{id_td}" 
                hx-swap="innerHTML" hx-get="table_view/edit?id_td={id_td}&id_grf={id_grf}">{rasp_id_visible}
            </div>
        """
        return response  
    else:
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
            
        sel_2 = ['<option value="0">Не назначен</option>', ] 
        for i in range(1, len(result_time)):
            sel2_vol = f"""<option value="{result_time[i][0]}">{result_time[i][1]}</option>"""
            sel_2.append(sel2_vol)
                
        response = f"""<div id="modal-backdrop" class="modal-backdrop fade show" style="display:block;"></div>
                        <div id="modal" class="modal fade show" tabindex="-1" style="display:block;">
                            <div class="modal-dialog modal-dialog-centered modal-lg">
                            <div class="modal-content">
                                <div class="modal-header">
                                <h5 class="modal-title">Сотрудник</h5>
                                </div>
                                <form hx-post="grf_insWorkerTable?otd={otd}&year={y}&month={m}" action=""> 
                                <div class="modal-body">
                                       
                                        <table class="table table-borderless">
                                            <tr>
                                                <td style="text-align: center; width:50%;">
                                                    <label class="custom-select-label" for="worker_select">Сотрудник</label> 
                                                    <select class="custom-select" id="worker_select"  name = "worker_select">                                                
                                                        {sel_doc}
                                                    </select>
                                                    
                                                    <label class="custom-select-label" for="room_select">№ кабинета</label> 
                                                    <select class="custom-select" id="room_select"  name = "room_select">                                                
                                                        {sel_room}
                                                    </select>
                                                    
                                                    <div class="mb-3">
                                                        <label class="col-form-label">Норма часов в месяц:</label>
                                                        <input type="number" class="form-control" name="UpdNclock">
                                                    </div>    
                                                </td>                                                
                                            </tr>
                                        </table>
   
                                        </div>
                                        <div class="modal-footer">
                                            <table class="table table-borderless">
                                                <tr>
                                                    <td style="text-align: left;">
                                                      <button class="btn btn-primary btn-success" type="submit" onclick="closeModal()">Сохранить</button>  
                                                    </td>                                            
                                                    <td style="text-align: right;"> 
                                                        <button type="button" class="btn btn-danger" onclick="closeModal()">&nbsp;Отмена&nbsp;</button> 
                                                    </td>                                            
                                                </tr>
                                        </div>
                                         
                                </div>                                  
                            </div>
                        </div>
                     </div>
                     </form>
                     </div>"""
        return response

@htmx_test.route('/grf_insWorkerTable', methods=['GET', 'POST'])
def grf_insWorkerTable():
        #добавить новую запись в таблицу IT_RASP_GRF
        procedure_name = 'NEW_GEN_IT_RASP_GRF_ID'
        output_params = db.proc(procedure_name)[0]
        otd = request.args.get('otd') #код отделения
        lpu = int(db.select(sql.sql_currentOtd.format(otd=otd))[0][2])
        y = request.args.get('year') #год
        m = request.args.get('month') #месяц       
        nclock = request.form.get('UpdNclock') #норма часов
        doc = request.form.get('worker_select') #код сотрудника
        spz = db.select(sql.sql_doctod.format(otd=otd, doc=doc))[0][2] 
        room = request.form.get('room_select') #номер кабинета
        new_data = f' LPU={lpu}, OTD={otd}, SPZ={spz}, DOC={doc}, YEARWORK={y}, MONTHWORK={m}, NCLOCK={nclock}, ROOM={room} '
        db.write(sql_upd_it_rasp_grf_.format(new_data=new_data, id_grf=output_params))
        return redirect(url_for("htmx_test.table_view", otd=otd, year=y, month=m))
    
        # id_td = request.args.get('id_td')
        # s_id_td = id_td[2:4]
        # s_id_td = f'day{s_id_td}'    
        # id_grf = request.args.get('id_grf')
        # rasp_id = request.form.get('rasp_id')
        # rasp_id_visible =db.select( sql.sql_interval_time_current.format(id=rasp_id))
        # rasp_id_visible = rasp_id_visible[0][0] 
        # response = f"""
        #     <div name="id_grf" 
        #         hx-target="#{id_td}" 
        #         hx-swap="innerHTML" hx-get="table_view/edit?id_td={id_td}&id_grf={id_grf}">{rasp_id_visible}
        #     </div>
        # """
        # return response  