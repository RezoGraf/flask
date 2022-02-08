from datetime import datetime
from flask import render_template, request, url_for, redirect, Blueprint, session
import pandas as pd
from . import report
from app.menu_script import generate_menu
import app.db as db
import app.sql as sql
import app.utils as utils

report = Blueprint('report', __name__)


@report.route('/', methods=['GET', 'POST'])
def main():
    if 'arena_mpp' not in session:
        return redirect(url_for("login"))
    else:
        if request.method == 'POST':
            # dtn = request.form.get('dtn')
            dtn = request.form.get('dtn_get')
            dtk = request.form.get('dtk_get')
            select_otd = request.form.get('select_otd')
            dtn_simple = pd.Timestamp(request.form.get('dtn_get'))
            dtk_simple = pd.Timestamp(request.form.get('dtk_get'))
            if request.form['btn'] == 'saveToPdf':
                return redirect(url_for('excel.excel_ots', _external=True, dtn=dtn_simple.strftime("%d.%m.%Y"),
                                        dtk=dtk_simple.strftime("%d.%m.%Y"),
                                        select_otd=select_otd))
            else:
                return redirect(url_for('report.main',
                                        dtn=dtn,
                                        dtk=dtk,
                                        select_otd=select_otd))
        else:
            dtn_simple = request.args.get('dtn')
            dtk_simple = request.args.get('dtk')
            dtn = request.args.get('dtn')
            dtk = request.args.get('dtk')
            select_otd = request.args.get('select_otd')
            result = ''
            select_current_ord = ''
            result = ('','','','','')
            if dtn is None:
                dtn = datetime.today().strftime('%d.%m.%Y')
                dtn_simple = datetime.today().strftime('%Y-%m-%d')
            if dtn_simple is None:
                dtn_simple = datetime.today().strftime('%Y-%m-%d')
            if dtk is None:
                dtk = datetime.today().strftime('%d.%m.%Y')
            if dtk_simple is None:
                dtk_simple = datetime.today().strftime('%Y-%m-%d')
            if select_otd is None or select_otd == 0 or select_otd == '0':
                select_current_ord = ([0, "Все отделения", 0],)
                result = db.select(sql.sql_select_otsut.format(date_start=dtn, date_finish=dtk))
            else:
                select_otd2=(f'and otd in({select_otd})')
                select_current_ord = db.select(sql.sql_allOtd.format(select_otd=select_otd2))
                result = db.select(sql.sql_select_otsut_otd.format(date_start=dtn, date_finish=dtk, otd=select_otd2))
            arena_user = session.get('arena_user')
            allow_otd = utils.access_user_otd(arena_user)
            select_allow_otd = db.select(sql.sql_allOtd.format(select_otd=allow_otd))
            menu = generate_menu()
            return render_template("report.html",
                                   my_list=result, dtn_get=dtn_simple, dtk_get=dtk_simple,
                                   menu=menu, result_select=select_allow_otd,
                                   select_current_ord=select_current_ord)
