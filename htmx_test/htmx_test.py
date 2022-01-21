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
    table_view_all = db.select(sql.sql_htmx_text_tablevew)
    otd=12
    return render_template("htmx_tableview.html", table_view_all=table_view_all)


@htmx_test.route("/table_view/edit")
def table_edit():
    # list_of_time = db.select(sql.sql_interval_time)
    # list_of_options = ''
    i = 1
    while i < len(list_of_time):
        option = f'<option value="{list_of_time[i][0]}">{list_of_time[i][1]}</option>'
        list_of_options = f'{list_of_options + option}'
    print (list_of_options)
    # response = """<div>
    #     <label >Make</label>
    #     <select name="make" hx-get="/models" hx-target="#models" hx-indicator=".htmx-indicator">
    #     <option value="audi">Audi</option>
    #     <option value="toyota">Toyota</option>
    #     <option value="bmw">BMW</option>
    #     </select>
    # </div>"""
    response = """<div>
                <label >Make</label>
                <select name="make" hx-get="/models" hx-target="#models" hx-indicator=".htmx-indicator">
                  <option value="audi">Audi</option>
                  <option value="toyota">Toyota</option>
                  <option value="bmw">BMW</option>
                </select>
              </div>"""
    return response
