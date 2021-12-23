import db
import models
import sql
from api.api import api
from data_input.data_input import data_input
from flask import Flask, render_template, request, url_for, redirect
from flask import Blueprint, render_template, abort, redirect, url_for, request
# регистрируем схему `Blueprint`
from data_input.models import SignupForm, WtfTemplate, WtfTemplate2, WtfTemplate3
from data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc
from data_input.sql_data_input import sql_ins_rsp_blc, sql_ins_it_rasp_duty
from . import report
import pandas as pd
from datetime import datetime
import db
import sql
import utils
import calendar


report = Blueprint('report', __name__)


@report.route("/", methods=['GET', 'POST'])
def main():
    dtn = request.args.get('dtn')  # запрос к данным формы
    dtk = request.args.get('dtk')
    if dtn is None:
        dtn = datetime.today().strftime('%d.%m.%Y')
        # dtn = datetime.today()
        # dtn = '01.12.2021'
    if dtk is None:
        # dtk = '07.12.2021'
        dtk = datetime.today().strftime('%d.%m.%Y')
    if request.method == 'POST':
        # dtn = request.form.get('dtn')
        dtn = pd.Timestamp(request.form.get('dtn'))  # запрос к данным формы
        dtk = pd.Timestamp(request.form.get('dtk'))
        # dtn.strftime("%d.%m.%Y")
        # dtk.strftime("%d.%m.%Y")
        if request.form['btn'] == 'saveToPdf':
            # dtn = request.form.get('dtn')  # запрос к данным формы
            # dtk = request.form.get('dtk')
            return redirect(url_for('excel.excel_ots', _external=True, dtn=dtn.strftime("%d.%m.%Y"), dtk=dtk.strftime("%d.%m.%Y")))
        return redirect(url_for('report.main',
                                dtn=dtn,
                                dtk=dtk))
    result = db.select(sql.sql_select.format(dtn=dtn,
                                                dtk=dtk))
    print(type(result))
    return render_template("report.html",
                           my_list=result, dtn=dtn, dtk=dtk)
