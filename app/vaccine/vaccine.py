"""Модуль Вакцинация"""
import time
from loguru import logger
from app.utils import db_to_html_table
import app.db as firebird
from app.auth import login_required
from flask import Blueprint, render_template, request, redirect, url_for, session
import app.vaccine.sql_vaccine as sql_vaccine
from app import db_pg


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
    data = firebird.sel_dict_in_turple_desc(sql_vaccine.select_all_mpp)
    # print(data[0])
    option = '<option selected value={mpp}>{fam} {im} {ot}</option>'
    # print(option)
    # for i, _ in enumerate(data):
    #     db_pg.write(sql_vaccine.sinc_worker.format(mpp = data[i]['MPP'],
    # fam = data[i]['FAM'], im = data[i]['IM'], ot = data[i]['OT'], lpu = data[i]['LPU'],
    # otd = data[i]['OTD'], dolj = data[i]['DOLJ'], spz=data[i]['SPZ'], sdl=data[i]['SDL']))
    # spz_fb = firebird.sel_dict_in_turple_desc(sql_vaccine.select_spz)
    # for i, _ in enumerate(spz_fb):
    #     db_pg.write(sql_vaccine.sinc_spz.format(id=spz_fb[i]['SPZ'],nspz=spz_fb[i]['NSPZ']))
    # otd_fb = firebird.sel_dict_in_turple_desc(sql_vaccine.select_otd)
    # for i, _ in enumerate(otd_fb):
    #     db_pg.write(sql_vaccine.sinc_otd.format(id=otd_fb[i]['OTD'],notd=otd_fb[i]['NOTD'],
    #                                     notd_kr=otd_fb[i]['NOTD_KR'],lpu=otd_fb[i]['LPU']))
    # sdl_fb = firebird.sel_dict_in_turple_desc(sql_vaccine.select_sdl)
    # for i, _ in enumerate(sdl_fb):
    #     db_pg.write(sql_vaccine.sinc_sdl.format(id=sdl_fb[i]['SDL'],nsdl=sdl_fb[i]['NSDL']))
    # dolj_fb = firebird.sel_dict_in_turple_desc(sql_vaccine.select_dolj)
    # for i, _ in enumerate(dolj_fb):
    #     print(dolj_fb)
    #     db_pg.write(sql_vaccine.sinc_dolj.format(id=dolj_fb[i]['DLJ'],ndlj=dolj_fb[i]['NDLJ']))
    # podr_fb = firebird.sel_dict_in_turple_desc(sql_vaccine.select_podr)
    # for i, _ in enumerate(podr_fb):
    #     db_pg.write(sql_vaccine.sinc_podr.format(id=podr_fb[i]['LPU'],npodr=podr_fb[i]['SNLPU']))
    #     print(podr_fb[i])
    # vaccine_fb = firebird.sel_dict_in_turple_desc(sql_vaccine.select_vaccine)
    # for x in range(len(vc)):
    #   db_pg.write(sql_vaccine.sinc_vaccine.format(nvc=vc[x]['NVVC'], vcid=vc[x]['VVC']))
    #   x += 1
    if request.method == 'POST':
        as_list = request.form.getlist('exampleFormControlSelect2')
        data = firebird.sel_dict_in_turple_desc(sql_vaccine.select_all_mpp)
        for worker in as_list:
            one_worker = firebird.sel_dict_in_turple_desc(
                sql_vaccine.select_one_mpp.format(mpp=int(worker)))
            # print(one_worker)
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
    response = """<div id="loading_from_firebird" hx-get="/vaccine/load_from_fb_data"
            hx-trigger="load">
			<img  alt="Result loading..." class="htmx-indicator" width="150"
            src="/static/img/bars.svg"/>
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
    menu = session['menu']
    return render_template('vaccine.html', menu=menu)


@vaccine.route('/vaccine_select', methods=['GET','POST'])
@login_required
@logger.catch
def vaccine_select():
    """Загрузка фильтров для сортировки и поиска

    Returns:
        response: html с двумя select
    """
    # if request.method == 'POST':
    #     search = ''
    #     if request.form.get('search') != '':
    #         search = request.form.get('search')
    #     if request.form.get('podr_select') != (0, '0' ,None):
    #         podr = request.form.get('podr_select')
    #     else:
    #         podr = 0
    #     if request.form.get('otd_select') != (0, '0' ,None):
    #         otd = request.form.get('otd_select')
    #     else:
    #         podr = 0
    #     return redirect(url_for('vaccine.vaccine_select',
    #                             podr=podr,
    #                             otd=otd,
    #                             search=search))
    search = request.args.get('search')
    podr = request.args.get('podr')
    otd = request.args.get('otd_select')
    print(f'search={search},podr={podr},otd{otd}')
    response = """
    <div id="search_results">
        <form>
            <div class="container">
                <div class="row">
                    <input class="form-control" autocomplete="off" type="search"
                        name="search" placeholder="Искать..."
                        hx-post="/vaccine_table"
                        hx-trigger="keyup changed delay:500ms, search"
                        hx-target="#table_main"
                        hx-indicator=".htmx-indicator">
                    <label class="col" for="podr_select">Подразделение</label>
                    <div class="col">
                        <select id="podr_select" name="podr_select" class="form-control">
                            <option value="1" selected>Все</option>
                        </select>
                    </div>
                    <label class="col" for="otd_select">Отделение</label>
                    <div class="col">
                        <select id="otd_select" name="otd_select" class="form-control">
                            <option value="1" selected>Все</option>
                        </select>
                    </div>
                </div>
            </div>
        </form>
    </div>"""
    return response


@vaccine.route('/vaccine_table', methods=['GET','POST'])
@login_required
@logger.catch
def vaccine_table():
    """Формирование таблицы сотрудников

    Returns:
        response: html <tbody> </tbody>
    """
    data = db_pg.sel_dict_in_list_desc(sql_vaccine.select_workers_main)
    table_head = """
    <table id="table_main" class="table table-striped">
    <thead>
    <th>ФИО</th>
    <th>Подразделение</th>
    <th>Отделение</th>
    <th>Должность</th>
    <th>Сертификат</th>
    </thead>"""
    table_body = db_to_html_table(data, tr=['IDW','s'],
                                        nulls=['Отсутствует'],
                                        cols=['FIO','NPODR','NOTD','NDLJ','CERT']
                                        )
    response = f"""{table_head} {table_body} </table"""
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
    data = firebird.sel_dict_in_turple_desc(sql_vaccine.select_all_mpp)
    option = '<option selected value={mpp}>{fam} {im} {ot}</option>'
    strings = ''
    for i in range(data):
        # db_pg.write(sql_vaccine.sinc_worker.format(mpp=data[i]['MPP'], fam=data[i]['FAM'],
        # im = data[i]['IM'], ot = data[i]['OT'], lpu=data[i]['LPU'], otd=data[i]['OTD'],
        # dolj=data[i]['DOLJ']))
        strings += option.format(mpp=data[i]['MPP'], fam = data[i]['FAM'],
                                im = data[i]['IM'], ot = data[i]['OT'])
    vaccine2 = firebird.sel_dict_in_turple_desc(sql_vaccine.select_vaccine)
    # print(vaccine2[0])
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
    # workers = request.form.get['workers_for_load']
    # print(workers)
    response = """<div id="loading_to_pg" hx-get="/vaccine/load_to_pg_data" hx-trigger="load">
            <img  alt="Result loading..." class="htmx-indicator" width="150" src="/static/img/bars.svg"/>
            </div>"""
    return response


@vaccine.route('/load_to_pg_data')
@login_required
@logger.catch
def load_to_pg_data():
    """Загрузка данных в pg

    Returns: response: Any"""
    time.sleep(1)
    data = firebird.sel_dict_in_turple_desc(sql_vaccine.select_all_mpp)
    option = '<option selected value="{var}">{var}</option>'
    sets = ''
    for i in range(data):
        sets += option.format(var=data[i])
    response = f"""
    <div class="form-group">
    <label for="exampleFormControlSelect3">Пример множественного выбора</label>
    <select id="select_multiple" multiple class="form-control" id="exampleFormControlSelect3" name="workers_for_load">
        {sets}
    </select>
    <button name="btn" value="load_from_fb_mpp" type="submit">Загрузить</button>
    </div>"""
    return response
