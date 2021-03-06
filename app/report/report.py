"""Отчеты по отсутствующим на рабочем месте"""
from datetime import datetime
from loguru import logger
import pandas as pd
from flask import render_template, request, url_for, redirect, Blueprint, session
from app.auth import login_required
import app.db as db
import app.sql as sql
import app.utils as utils


report = Blueprint('report', __name__)


@report.route('/', methods=['GET', 'POST'])
@login_required
@logger.catch
def main():
    """Отчет по отсутствующим

    Returns:
        render_template: report.html
    """
    # if 'arena_mpp' not in session:
    #     return redirect(url_for("login"))
    # else:
    if request.method == 'POST':
        dtn = request.form.get('dtn_get')
        dtk = request.form.get('dtk_get')
        podr_select = request.form.get('podr_select')
        select_otd = request.form.get('select_otd')
        dtn_simple = pd.Timestamp(request.form.get('dtn_get'))
        dtk_simple = pd.Timestamp(request.form.get('dtk_get'))
        if request.form['btn'] == 'saveToPdf':
            return redirect(url_for('excel.excel_ots',
                                    _external=True,
                                    dtn=dtn_simple.strftime("%d.%m.%Y"),
                                    dtk=dtk_simple.strftime("%d.%m.%Y"),
                                    select_otd=select_otd,
                                    podr_select=podr_select,
                                    ))
        else:
            return redirect(url_for('report.main',
                                    dtn=dtn,
                                    dtk=dtk,
                                    select_otd=select_otd,
                                    podr_select=podr_select))
    else:
        dtn_simple = request.args.get('dtn')
        dtk_simple = request.args.get('dtk')
        dtn = request.args.get('dtn')
        dtk = request.args.get('dtk')
        lpu = request.args.get('podr_select')
        select_otd = request.args.get('select_otd')
        podr_select = request.args.get('podr_select')
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

        podr_all = db.select(sql.sql_select_podr)

        if podr_select in (None, 0, '0'):
        # if podr_select is None or podr_select == 0 or podr_select == '0':
            podr_select = ([0, "Все подразделения"],)
            if select_otd in (None, 0, '0'):
            # if select_otd is None or select_otd == 0 or select_otd == '0':
                select_current_ord = ([0, "Все отделения", 0],)
                result = db.select(sql.sql_select_otsut.format(
                                        date_start=dtn,
                                        date_finish=dtk))
            else:
                select_otd2=(f'and otd in({select_otd})')
                select_current_ord = db.select(sql.SQL_ALLOTD.format(
                                        select_otd=select_otd2))
                result = db.select(sql.sql_select_otsut_otd.format(
                                        date_start=dtn,
                                        date_finish=dtk,
                                        otd=select_otd2))
        else :
            podr_select = db.select(sql.sql_select_podr_one.format(
                                        lpu=podr_select))
            i = 0
            for podr in podr_all:
                if podr[0] != podr_select[0][0]:
                    i = i+1
            _ = podr_all.pop(i)
            podr_all.insert(0, (0, "Все подразделения"))
            if select_otd in (None, 0, '0'):
            # if select_otd is None or select_otd == 0 or select_otd == '0':
                select_current_ord = ([0, "Все отделения", 0],)
                result = db.select(sql.sql_select_otsut_lpu.format(
                                        date_start=dtn,
                                        date_finish=dtk,lpu=lpu))
            else:
                select_otd2=(f'and otd in({select_otd})')
                select_current_ord = db.select(sql.SQL_ALLOTD.format(
                                        select_otd=select_otd2))
                result = db.select(sql.sql_select_otsut_otd_lpu.format(
                                        date_start=dtn,
                                        date_finish=dtk,
                                        lpu=lpu,
                                        otd=select_otd))

        arena_user = session.get('arena_user')
        allow_otd = utils.access_user_otd(arena_user)
        select_allow_otd = db.select(sql.SQL_ALLOTD.format(
                                        select_otd=allow_otd))
        menu = session['menu']
        return render_template("report.html",
                                        podr_select=podr_select,
                                        my_list=result,
                                        dtn_get=dtn_simple,
                                        dtk_get=dtk_simple,
                                        menu=menu,
                                        result_select=select_allow_otd,
                                        select_current_ord=select_current_ord,
                                        podr_all=podr_all)


@report.route('/otd_by_lpu_list')
@logger.catch
def otd_by_lpu_list():
    """Выпадающий список отделений

    Returns:
        response: html option
    """
    lpu = request.args.get('podr_select')
    list_of_otd = db.select(sql.sql_allOtd_for_lpu.format(lpu=lpu))
    select_string = """<option value="{id}" > {name} </option>"""
    selected_string = """<option value="{id}" selected> {name} </option>"""
    select_strings = ''
    for one_of_list in list_of_otd:
        string = select_string.format(id=one_of_list[0],name=one_of_list[1])
        select_strings += string
    selected_strings = selected_string.format(id=0,name="Все отделения")
    response = f"""<select class="form-select" id="select_otd"
    name="select_otd">{select_strings}{selected_strings}</select>"""
    return response
    