from datetime import datetime
from flask import render_template, request, url_for, redirect, Blueprint, session
import pandas as pd
# from excel.excel import excel
# from data_input.data_input import data_input
from . import report
from app.menu_script import generate_menu
import app.db as db
import app.sql as sql

report = Blueprint('report', __name__)


@report.route('/', methods=['GET', 'POST'])
def main():
    if 'arena_mpp' in session:
        if request.method == 'POST':
            # dtn = request.form.get('dtn')
            dtn = request.form.get('dtn_get')
            dtk = request.form.get('dtk_get')
            dtn_simple = pd.Timestamp(request.form.get('dtn_get'))
            dtk_simple = pd.Timestamp(request.form.get('dtk_get'))
            # dtn.strftime("%d.%m.%Y")
            # dtk.strftime("%d.%m.%Y")
            if request.form['btn'] == 'saveToPdf':
                # dtn = request.form.get('dtn')  # запрос к данным формы
                # dtk = request.form.get('dtk')
                return redirect(url_for('excel.excel_ots', _external=True, dtn=dtn_simple.strftime("%d.%m.%Y"),
                                        dtk=dtk_simple.strftime("%d.%m.%Y")))
            else:
                return redirect(url_for('report.main',
                                        dtn=dtn,
                                        dtk=dtk))
        else:
            dtn_simple = request.args.get('dtn')
            dtk_simple = request.args.get('dtk')
            dtn = request.args.get('dtn')  # запрос к данным формы
            dtk = request.args.get('dtk')
            if dtn is None:
                dtn = datetime.today().strftime('%d.%m.%Y')
                dtn_simple = datetime.today().strftime('%Y-%m-%d')
                # dtn = datetime.today()
                # dtn = '01.12.2021'
            if dtn_simple is None:
                dtn_simple = datetime.today().strftime('%Y-%m-%d')
            if dtk is None:
                # dtk = '07.12.2021'
                dtk = datetime.today().strftime('%d.%m.%Y')
            if dtk_simple is None:
                dtk_simple = datetime.today().strftime('%Y-%m-%d')
            if 'arena_user' in session:
                arena_user = session.get('arena_user')
            else:
                arena_user = 'none'
            if 'arena_fio' in session:
                arena_fio = session.get('arena_fio')
            else:
                arena_fio = "Не пользователь домена"
            if 'auth_group' in session:
                auth_group = session.get('auth_group')
            else:
                auth_group = 'none'
            result = db.select(sql.sql_select_otsut.format(date_start=dtn,
                                                     date_finish=dtk))
            menu = generate_menu()
            return render_template("report.html",
                                   my_list=result, dtn_get=dtn_simple, dtk_get=dtk_simple,
                                   arena_fio=arena_fio, menu=menu)
    else:
        return redirect(url_for("app.login"))
