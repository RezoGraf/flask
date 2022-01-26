from flask import Flask, render_template, request, Blueprint
import json
import os.path
import db, sql
from data_input.sql_data_input import sql_upd_it_rasp_grf
from dateutil import parser
from datetime import date
import calendar
import utils

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
    return render_template("htmx_test.html", items=data)


@htmx_test.route("/table_view")
def table_view():
    """отображение таблицы с расписанием, ничего интересного
    Returns:
        html страницу (htmx_tableview.html) с таблицей, смотреть внимательно
    """    
    current_date = date.today()
    current_year = parser.parse(current_date.strftime('%m/%d/%y')).strftime("%Y")
    current_month = parser.parse(current_date.strftime('%m/%d/%y')).strftime("%m")
    all_day = calendar.monthrange(int(current_year), int(current_month))[1]
    # result_otd = db.select(sql.sql_allOtd) 
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
            value_ = f"""{p}  {pa}""" 
            key_ = f'day{str(i)}'
            if pa=='Вс.' or pa=='Сб.' :
                class_th='table-success'
            else:
                class_th='table-light'
            result_th[key_] = [class_th,value_]  
    otd=12           
    # table_view_all = db.select(sql.sql_TabelWorkTime.format(otd=otd, EYear=current_year, EMonth=current_month))
    table_view_all = db.select_dicts_in_turple(sql.sql_TabelWorkTime.format(otd=otd, EYear=current_year, EMonth=current_month))      
    return render_template("htmx_tableview.html", 
                           table_view_all = table_view_all,
                           result_th = result_th)


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
        # if int(s_id_td)<10 :
        # s_id_td = s_id_td[1:2]
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
