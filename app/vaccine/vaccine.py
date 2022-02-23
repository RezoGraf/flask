"""Модуль Вакцинация"""
import time
from loguru import logger
import app.db as firebird
from app.auth import login_required
from flask import Blueprint, render_template, request, redirect, url_for, session
import app.db_pg as db_pg
import app.vaccine.sql_vaccine as sql_vaccine
import app.utils as utils


vaccine = Blueprint('vaccine', __name__)


@vaccine.route('/sinc', methods=['GET', 'POST'])
@login_required
@logger.catch
def sinc():
	"""Синхронизация справочников fb - pg
	Returns:
		render_template: vaccine_loader.html
	"""	
	menu = session['menu']
	data = firebird.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
	print(data[0])
	option = '<option selected value={mpp}>{fam} {im} {ot}</option>'
	print(option)
	s_str = ''
	print(s_str)
    # for i in range(len(data)):
    #   print(sql_vaccine.sinc_worker.format(mpp = data[i]['MPP'], fam = data[i]['FAM'], im = data[i]['IM'], ot = data[i]['OT'], lpu = data[i]['LPU'], otd = data[i]['OTD'], dolj = data[i]['DOLJ']))
    #   db_pg.write(sql_vaccine.sinc_worker.format(mpp = data[i]['MPP'], fam = data[i]['FAM'], im = data[i]['IM'], ot = data[i]['OT'], lpu = data[i]['LPU'], otd = data[i]['OTD'], dolj = data[i]['DOLJ']))
	vaccine_fb = firebird.select_dicts_in_turple_with_description(sql_vaccine.select_vaccine)
	print(vaccine_fb[0])
    # for x in range(len(vc)):
    #   db_pg.write(sql_vaccine.sinc_vaccine.format(nvc=vc[x]['NVVC'], vcid=vc[x]['VVC']))
    #   x += 1
	if request.method == 'POST':
		as_list = request.form.getlist('exampleFormControlSelect2')
		data = firebird.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
		
		for x in as_list:
			one_worker = firebird.select_dicts_in_turple_with_description(sql_vaccine.select_one_mpp.format(mpp=int(x)))
		return redirect(url_for('vaccine.sinc'))
	else:
		return render_template('vaccine_loader.html', menu=menu)


@vaccine.route('/load_from_fb')
@login_required
@logger.catch
def load_from_fb():
	"""Функция вызывает htmx load для загрузки данных из бд fb

	Returns:
		response: html код htmx load
	"""
	response = """<div id="loading_from_firebird" hx-get="/vaccine/load_from_fb_data" hx-trigger="load">
			<img  alt="Result loading..." class="htmx-indicator" width="150" src="/static/img/bars.svg"/>
			</div>"""
	return response


@vaccine.route('/vaccine_main')
@login_required
@logger.catch
def vaccine_main():
	"""Главная страница "Вакцинация"

	Returns:
		render_template: vaccine.html
	"""
	# all_otd = db.select(sql_vaccine.)
	# select_otd = """<option selected></option>"""
	# for x in all_otd:
	#     select_string = f"""<option style="font-size:15px">{x[0]}</option>"""
	#     select_otd += select_string
	# all_select_otd = f"""<select style="font-size:15px" class="form-select" name="reason_filter" id="myInputReason"
	# name="select_otd">{select_otd}</select>"""
	menu = session['menu']
	return render_template('vaccine.html', menu=menu)


@vaccine.route('/vaccine_table')
@login_required
@logger.catch
def vaccine_table():
    """Формирование таблицы сотрудников

    Returns:
        response: html <tbody> </tbody>
    """
    data = db_pg.select_dicts_in_list_with_description(sql_vaccine.select_workers)
    string8 = utils.db_to_html_table(data, 5 {'cols':'col1','None'})
    print(string8)
    table_tr = """<thead>
    <th>ФИО</th>
    <th>Подразделение</th>
    <th>Отделение</th>
    <th>Должность</th>
    <th>Сертификат</th>
    </thead>
    <tbody>"""
    # x = 0
    for i in range(data):
        if data[i]['CERT'] is None:
            data[i]['CERT'] = 'Отсутствует'
            table_row = f"""<tr id="{data[i]['IDW']}">
            <td>{data[i]['FAM_WORKER']} {data[i]['IM_WORKER']} {data[i]['OT_WORKER']}</td>
            <td>{data[i]['PODR']}</td>
            <td>{data[i]['OTD']}</td>
            <td>{data[i]['DLJ']}</td>
            <td>{data[i]['CERT']}</td>
            </tr>"""
        table_tr += table_row
        table_row = ''
        # x += 1
    response = f"""{table_tr}
    </tbody>"""
    # response = {table_tr}
    return response


@vaccine.route('/load_from_fb_data')
@login_required
@logger.catch
def loaf_from_fb_data():
    """Загрузка данных из fb и запись в базу pg

    Returns:
        response: возвращает окно с выбором людей для загрузки
    """
    time.sleep(1)
    data = firebird.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
    option = '<option selected value={mpp}>{fam} {im} {ot}</option>'
    strings = ''
    for i in range(data):
        # db_pg.write(sql_vaccine.sinc_worker.format(mpp=data[i]['MPP'], fam=data[i]['FAM'],
        # im = data[i]['IM'], ot = data[i]['OT'], lpu=data[i]['LPU'], otd=data[i]['OTD'], dolj=data[i]['DOLJ']))
        strings += option.format(mpp=data[i]['MPP'], fam = data[i]['FAM'],
                                im = data[i]['IM'], ot = data[i]['OT'])

    vaccine2 = firebird.select_dicts_in_turple_with_description(sql_vaccine.select_vaccine)
    print(vaccine2[0])
    # for x in range(len(vc)):
    #   db_pg.write(sql_vaccine.sinc_vaccine.format(nvc=vc[x]['NVVC'], vcid=vc[x]['VVC']))
    #   x += 1
    response = f"""
    <div class="form-group">
    <br>
    <label for="exampleFormControlSelect2">Выберите сотрудников для загрузки</label>
    <select multiple size="20" class="form-control" id="exampleFormControlSelect2" name="exampleFormControlSelect2">
        {strings}
    </select>
    <br>
    <button class="btn btn-primary" type="submit">Загрузить сотрудников в БД Хелиос</button>
    </div>"""
    return response


@vaccine.route('/load_from_fb_to_pg', methods=['GET', 'POST'])
@login_required
@logger.catch
def load_from_fb_to_pg():
    """Загрузчик для загрузки данных из fb в pg

    Returns:
        response: html код htmx load для загрузки окно загрузки данных из fb
    """
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
	data = firebird.select_dicts_in_turple_with_description(sql_vaccine.select_all_mpp)
	utils.db_to_html_table(data, {'col':['CERT', 'пусто'],['FAM_WORKER', 'пусто']})
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