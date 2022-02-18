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
    print(all_today[0])
    return render_template('in_work.html', menu=menu, table = all_today)



# @in_work.route('/search_podr', methods=['GET', 'POST'])
# @login_required
# @logger.catch
# def search_podr():
#     table = db.select_dicts_in_turple_with_description(sql_in_work.sql)
