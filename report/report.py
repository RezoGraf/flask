import db
import models
import sql
from api.api import api
from data_input.data_input import data_input
from excel.excel import excel
from flask import Flask, render_template, request, url_for, redirect
from flask import Blueprint, render_template, abort, redirect, url_for, request
# регистрируем схему `Blueprint`
from data_input.models import SignupForm, WtfTemplate, WtfTemplate2, WtfTemplate3
from data_input.sql_data_input import sql_ins_rsp_blc, sql_del_rsp_blc, sql_upd_rsp_blc
from data_input.sql_data_input import sql_ins_rsp_blc, sql_ins_it_rasp_duty
from . import report
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
        dtn = '01.12.2021'
    if dtk is None:
        dtk = '07.12.2021'
    if request.method == 'POST':
        dtn = request.form.get('dtn')  # запрос к данным формы
        dtk = request.form.get('dtk')
        return redirect(url_for('report',
                                dtn=dtn,
                                dtk=dtk))
    # sql_select_filtered = sql.sql_select.format(dtn=dtn,
    #                                             dtk=dtk)
    result = db.select(sql.sql_select.format(dtn=dtn,
                                                dtk=dtk))
    print(type(result))
    return render_template("report.html",
                           my_list=result, dtn=dtn, dtk=dtk)