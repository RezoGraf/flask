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


vaccine = Blueprint('vaccine', __name__)


@vaccine.route('/sinc', methods=['GET', 'POST'])
# @login_required
# @logger.catch
def sinc():
    menu = session['menu']
    # as_list = []
    # if request.args.get['as_list'] is not None:
    #     as_list = request.args.get['as_list']
    # print(as_list)
    # s = request.args
    # print(s)
    # jsonData = request.get_json()
    # print(jsonData)
    # print(request.args)
    # workers = request.args.get
    # if request.args.get['workers'] is not None:
    #     workers = request.args.get['workers']
    #     for i in workers:
    #         print(i)
    # workers = ''
    # if request.form.get['workers'] is not None:
    # workers = request.args.get['workers']
        # return render_template('vaccine_write.html', menu=menu, workers=workers)
    if request.method == 'POST':
        # if request.form['btn'] == 'load_from_fb_mpp':
        # workers = request.form.get['workers_for_load']
        # as_dict = request.form.getlist('exampleFormControlSelect2')
        as_list = request.form.getlist('exampleFormControlSelect2')
        # print(as_list)
        data = db.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
        for x in as_list:
          print(int(x))
          one_worker = db.select_dicts_in_turple_with_description(sql_vaccine.select_one_mpp.format(mpp=int(x)))
          
        # print(as_list[0])
        # print(request)
        # for i in workers:
        #     print(i)
        # print(workers)
        return redirect(url_for('vaccine.sinc'))
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
    time.sleep(1)
    data = db.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
    option = '<option selected value={mpp}>{fam} {im} {ot}</option>'
    s = ''
    for i in range(len(data)):
        s += option.format(mpp=data[i]['MPP'], fam = data[i]['FAM'], im = data[i]['IM'], ot = data[i]['OT'])
        i += 1
    response = f"""
    <div class="form-group">
    <br>
    <label for="exampleFormControlSelect2">Выберите сотрудников для загрузки</label>
    <select multiple size="20" class="form-control" id="exampleFormControlSelect2" name="exampleFormControlSelect2">
      {s}
    </select>
    <br>
    <button class="btn btn-primary" type="submit">Загрузить сотрудников в БД Хелиос</button>
  </div>"""
    return response


@vaccine.route('/load_from_fb_to_pg', methods=['GET', 'POST'])
@login_required
@logger.catch
def load_from_fb_to_pg():
    workers = request.form.get['workers_for_load']
    print(workers)
    response = """<div id="loading_to_pg" hx-get="/vaccine/load_to_pg_data" hx-trigger="load">
            <img  alt="Result loading..." class="htmx-indicator" width="150" src="/static/img/bars.svg"/>
          </div>"""
    return response


@vaccine.route('/load_to_pg_data')
@login_required
@logger.catch
def load_to_pg_data():
    time.sleep(1)
    data = db.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
    option = '<option selected value="{var}">{var}</option>'
    s = ''
    for i in range(len(data)):
        s += option.format(var=data[i])
        i += 1
    response = f"""
    <div class="form-group">
    <label for="exampleFormControlSelect3">Пример множественного выбора</label>
    <select id="select_multiple" multiple class="form-control" id="exampleFormControlSelect3" name="workers_for_load">
      {s}
    </select>
    <button name="btn" value="load_from_fb_mpp" type="submit">Загрузить</button>
  </div>"""
    return response