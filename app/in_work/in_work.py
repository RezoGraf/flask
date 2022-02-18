from datetime import datetime
from flask import Blueprint, render_template, request, url_for, session
import app.db as db
import app.sql as sql
from app.auth import login_required
import logging
from loguru import logger
import app.in_work.sql_in_work as sql_in_work




in_work = Blueprint('in_work', __name__)


@in_work.route('/', methods=['GET', 'POST'])
@login_required
@logger.catch
def main():
    menu = session['menu']
    today = datetime.today().strftime('%d.%m.%Y')
    all_today = db.select_dicts_in_turple_with_description(sql_in_work.sql_all_today.format(today = today))
    
    all_otd = db.select(sql_in_work.sql_all_otd)
    select_otd = """<option selected></option>"""
    for x in all_otd:
        select_string = f"""<option style="font-size:15px">{x[0]}</option>"""
        select_otd += select_string
    all_select_otd = f"""<select style="font-size:15px" class="form-select" name="reason_filter" id="myInputReason"
    name="select_otd">{select_otd}</select>"""

    all_podr = db.select(sql_in_work.sql_all_podr)
    select_podr = """<option selected style="font-size:15px"></option>"""
    for x in all_podr:
        select_string = f"""<option style="font-size:15px">{x[0]}</option>"""
        select_podr += select_string
    all_select_podr = f"""<select style="font-size:15px" class="form-select" name="podr_filter" id="myInputPodr"
    name="select_otd">{select_podr}</select>"""

    return render_template('in_work.html', menu=menu, table = all_today, all_select_otd=all_select_otd, all_select_podr=all_select_podr)



# @in_work.route('/search_podr', methods=['GET', 'POST'])
# @login_required
# @logger.catch
# def search_podr():
#     table = db.select_dicts_in_turple_with_description(sql_in_work.sql)
