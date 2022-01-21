from flask import Flask, render_template, request, Blueprint
import json
import os.path
import db, sql

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
    table_view_all = db.select(sql.sql_htmx_text_tablevew)
    otd=12
    return render_template("htmx_tableview.html", table_view_all=table_view_all)



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
        rasp_id = request.form.get('rasp_id')
        id_grf = request.form.get('id_grf')
        response = f"""
        <form id="td{id_grf}">
            <div name="id_grf" 
                value="{id_grf}" hx-target="#td{id_grf}" 
                hx-swap="outerHTML" hx-get="table_view/edit">{rasp_id}
            </div>
        </form>
        """
        return response
    else:
        id_grf = request.form.get('id_grf')
        list_of_time = db.select(sql.sql_interval_time)
        print(len(list_of_time))
        list_of_options = ''
        i = 1
        while i < (len(list_of_time)):
            option = f"""<option value="{list_of_time[i][0]}">{list_of_time[i][1]}</option>"""
            list_of_options = list_of_options + option
            i += 1
        print (list_of_options)
        response = f"""
            <form id="td{id_grf}">
                <div>
                    <select name="rasp_id" hx-post="table_view/edit" 
                        hx-target="#td{id_grf}" hx-indicator=".htmx-indicator">
                        {list_of_options}
                    </select>
                </div>
            </form>
            """
        return response
