"""Набор функций упрощающий жизнь"""

from dateutil import parser
from app import db, sql


def list_to_int(list_result) -> int:
    """Принимает список с одним значением и возвращает число

    Args:
        list_result (list): Список с одним значением

    Returns:
        int: число
    """
    string_result = ''.join(str(e) for e in list_result)
    string_result = string_result.replace('(', '')
    string_result = string_result.replace(')', '')
    string_result = string_result.replace(',', '')
    string_result = int(string_result)
    return string_result


def list_to_str(list_result) -> int:
    """Принимает список с одним значением и возвращает строку

    Args:
        list_result (list): Список с одним значением

    Returns:
        str: строка
    """
    string_result = ''.join(str(e) for e in list_result)
    string_result = string_result.replace('(', '')
    string_result = string_result.replace(')', '')
    string_result = string_result.replace(',', '')
    string_result = string_result.replace("'", '')
    return string_result


def russian_name_day_week(day_week):
    """Принимает день недели на английском и возвращает на русском

    Args:
        day_week (str): текстовое название дня недели на английском

    Returns:
        str: название дня недели на русском (краткое)
    """
    russian_day_week = {
        'Mon':'Пн.',
        'Tue':'Вт.',
        'Wed':'Ср.',
        'Thu':'Чт.',
        'Fri':'Пт.',
        'Sat':'Сб.',
        'Sun':'Вс.'
        }
    latin_name_dayweek = parser.parse(day_week).strftime("%a")
    result = russian_day_week[latin_name_dayweek]
    return result


def date_color(current_date):
    """_summary_

    Args:
        current_date (_type_): _description_

    Returns:
        _type_: _description_
    """
    dat = parser.parse(current_date)
    current_day = parser.parse(dat.strftime('%m/%d/%y')).strftime("%d")
    current_year = parser.parse(dat.strftime('%m/%d/%y')).strftime("%Y")
    current_month = parser.parse(dat.strftime('%m/%d/%y')).strftime("%m")
    russian_day_week = {
        'Mon':'Пн.',
        'Tue':'Вт.',
        'Wed':'Ср.',
        'Thu':'Чт.',
        'Fri':'Пт.',
        'Sat':'Сб.',
        'Sun':'Вс.'
        }
    dat = f'{str(current_day)}.{str(current_month)}.{str(current_year)}'
    ans = parser.parse(dat).strftime("%a")
    pas = russian_day_week[ans]
    result = ''
    if pas in ('Вс.','Сб.'):
        result = 'table-success'
    else:
        result = 'table-light'
    return result


def access_user_otd(arena_user) -> str:
    """Данные для формирования запроса по доступным отделениям

    Args:
        arena_user (str): Имя пользователя Arena

    Returns:
        str: часть запроса с доступными отделениями
    """
    result_accessotd = db.select(sql.sql_accessOtd.format(arena_user=arena_user))[0][0]

    if  result_accessotd != '0':
        select_otd=f' and otd in({result_accessotd})' #доступные отделения
    else:
        select_otd = ''

    return select_otd


def access_user_sdl(arena_user) -> str:
    """_summary_

    Args:
        arena_user (_type_): _description_

    Returns:
        str: _description_
    """
    result_access_sdl = db.select(sql.sql_accessSdl.format(arena_user=arena_user))[0][0]

    if  result_access_sdl != '0':
        select_sdl=f' and n_doc.sdl in ({result_access_sdl})' #доступные отделения
    else:
        select_sdl = ''

    return select_sdl


def db_to_html_tbody(data, tbody_id=None, htmx_func=None, **params) -> str:
    """Формирует tbody html

    Args:
        data (list): Выборка таблицы с заголовками
        tbody_id (str, optional): ID для таблицы. Defaults to None.
        tr=['ID', htmx=ID]: Список с параметрами для tr, ID - имя столбца БД
        nulls=['Отсутствует'],
        cols=['FIO','NPODR','NOTD','NDLJ','CERT']

    Returns:
        response: html <tbody></tbody>
    """
    tbody_id_tag = ''
    if tbody_id is not None:
        tbody_id_tag = f"""id="{tbody_id}" """
    else: tbody_id_tag = ''
    tbody_open = f"""<tbody {tbody_id_tag}>"""
    tbody_close = '</tbody>'
    table_body = ''
    table_tr_open = ''
    table_tr_close = '</tr>'
    for i, _ in enumerate(data):
        for key, param in params.items():
            if key == 'tr':
                param1 = f""" hx-get="{htmx_func}?idw={data[i][param[0]]}" {param[1]}" """
                table_tr_open = f"""<tr id={data[i][param[0]]} {param1}>"""
                # print(table_tr_open)
                break
            # else:
            #     pass
        table_body += table_tr_open
        # table_rows = ''
        for key, param in params.items():
            if key == 'cols':
                table_row = ''
                for j, _ in enumerate(param):
                    table_row += f"""<td>{data[i][param[j]]}</td>"""
                # table_rows += table_row
        table_body += table_row
        table_body += table_tr_close
    for key, param in params.items():
        if key == 'nulls':
            table_body = table_body.replace('None', param[0])
    table_done = f"""{tbody_open}{table_body}{tbody_close}"""
    return table_done
