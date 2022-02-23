"""Набор функций упрощающий жизнь"""
from dateutil import parser
import app.db as db
import app.sql as sql


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


def russianNameDayWeek(day_week):
    """Принимает день недели на английском и возвращает на русском

    Args:
        day_week (str): текстовое название дня недели на английском

    Returns:
        str: название дня недели на русском (краткое)
    """
    russianDayWeek = {'Mon':'Пн.' , 'Tue':'Вт.' , 'Wed':'Ср.' , 'Thu':'Чт.' , 'Fri':'Пт.' , 'Sat':'Сб.' , 'Sun':'Вс.'}
    latin_name_dayweek = parser.parse(day_week).strftime("%a")
    result = russianDayWeek[latin_name_dayweek]
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
    russian_day_week = {'Mon':'Пн.' , 'Tue':'Вт.' , 'Wed':'Ср.' , 'Thu':'Чт.' , 'Fri':'Пт.' , 'Sat':'Сб.' , 'Sun':'Вс.'}
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


def db_to_html_table(data = None, **params) -> str:
    """Формирование tbody из результата запроса

    Args:
        data (_type_, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    print(params)
    table_tr = """<tbody>"""
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
    table_tr += """</tbody"""
    return table_tr
    