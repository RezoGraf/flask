# from logging import Logger
from loguru import logger
from flask import Blueprint, render_template, request, redirect, url_for, session, g
from app.auth import login_required
from app.menu_script import generate_menu
from webargs import fields, validate
from webargs.flaskparser import use_args
import app.db as db
import app.vaccine.sql_vaccine as sql_vaccine
import time
# from . import vaccine


vaccine = Blueprint('vaccine', __name__)



# @use_args({"name": fields.Str(validate=[validate.Range(min=1, max=999)],required=True)}, location="query")


@vaccine.route('/sinc')
@login_required
@logger.catch
def sinc():
    menu = session['menu']
    if request.method == 'POST':
        if request.form['btn'] == 'load_from_fb_mpp':

            return redirect(url_for('vaccine.sinc', ))
    else:
        return render_template('vaccine_loader.html', menu=menu)


@vaccine.route('/load_from_fb')
@login_required
@logger.catch
def load_from_fb():
    response = """<div id="loading_from_firebird" hx-get="/vaccine/load_from_fb_data" hx-trigger="load">
            <img  alt="Result loading..." class="htmx-indicator" width="150" src="/static/img/bars.svg"/>
          </div>"""
    return response


@vaccine.route('/load_from_fb_data')
@login_required
@logger.catch
def loaf_from_fb_data():
    time.sleep(7)
    data = db.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
    option = '<option selected value="">{var}</option>'
    s = ''
    for i in range(len(data)):
        s += option.format(var=data[i])
        i += 1
    response = f"""
    <div class="form-group">
    <label for="exampleFormControlSelect2">Пример множественного выбора</label>
    <select multiple class="form-control" id="exampleFormControlSelect2">
      {s}
    </select>
  </div>"""
    # g.response = response
    # g['response'] = response
    return response
