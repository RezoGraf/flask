import calendar
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask import Blueprint, render_template, abort, redirect, url_for, request, session
import pandas as pd

from api.api import api
from data_input.data_input import data_input
from data_input.models import SignupForm, WtfTemplate, WtfTemplate2, WtfTemplate3
from data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc, sql_ins_it_rasp_duty 
from . import report

import models
import db
import sql
import utils


report = Blueprint('report', __name__)


@report.route('/', methods=['GET', 'POST'])
def main():

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
            return redirect(url_for('excel.excel_ots', _external=True, dtn=dtn_simple.strftime("%d.%m.%Y"), dtk=dtk_simple.strftime("%d.%m.%Y")))
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
            dtn_simple  = datetime.today().strftime('%Y-%m-%d')
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
        result = db.select(sql.sql_select.format(dtn=dtn,
                                             dtk=dtk))
        return render_template("report.html",
                           my_list=result, dtn_get=dtn_simple, dtk_get=dtk_simple,
                           arena_fio=arena_fio)