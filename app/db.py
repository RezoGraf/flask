"""Функции для работы с бд Firebird"""
from collections import defaultdict
import firebirdsql
from app.utils import date_color
import config


def select(sql):
    """Выборка из бд firebird

    Args:
        sql (str): sql запрос на выборку

    Returns:
        tuple: tuple с list внутри
    """
    con = firebirdsql.connect(dsn=config.dsn,
                              user=config.user,
                              password=config.password,
                              charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


def write(sql):
    """Запись данных в бд firebird

    Args:
        sql (str): sql запрос для записи данных в бд
    """
    con = firebirdsql.connect(dsn=config.dsn,
                              user=config.user,
                              password=config.password,
                              charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


def proc(proc_name):
    """Выполнение процедуры fb

    Args:
        proc_name (_type_): _description_

    Returns:
        tuple: возвращает результат выполнения процедуры
    """
    con = firebirdsql.connect(dsn=config.dsn,
                              user=config.user,
                              password=config.password,
                              charset=config.charset)
    cur = con.cursor()
    cur.callproc(proc_name)
    output_params = cur.fetchone()
    con.commit()
    return output_params


def select_dicts_in_turple(sql):
    """_summary_

    Args:
        sql (_type_): _description_

    Returns:
        _type_: _description_
    """    
    con = firebirdsql.connect(dsn=config.dsn,
                              user=config.user,
                              password=config.password,
                              charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    result = {}
    fieldIndices = range(len(cur.description))
    selectFields = ()
    for fieldDesc in cur.description:
        selectFields = *selectFields, fieldDesc[firebirdsql.DESCRIPTION_NAME]
    y = ''
    m = ''
    id = 0
    # result2 = {}
    result = defaultdict(list)
    for row in cur:
        color_ = 'table-light'
        for fieldIndex in fieldIndices:
            if 'ID_GRF' in selectFields[fieldIndex]:
                id = row[fieldIndex]
            if 'YEARWORK' in selectFields[fieldIndex]:
                y = row[fieldIndex]
            if 'MONTHWORK' in selectFields[fieldIndex]:
                m = str(row[fieldIndex])
                if len(m) == 1:
                    m = f'0{m}'
            if 'DAY' in selectFields[fieldIndex]:
                d = (selectFields[fieldIndex])[3:5]
                dc = f'{d}.{m}.{y}'
                color_ = date_color(dc)
                if row[fieldIndex] == None:
                    color_ = 'table-warning'
            key = f'{id}'
            # result[key] = [color_, row[fieldIndex]]
            result[key].append(color_)
            result[key].append(row[fieldIndex])
            # result[key] = (*result, result)

        # result2 = (*result2, result)
    cur.close()
    del cur
    return result


def select_dicts_in_turple2(sql):
    """Выборка данных из бд fb словарями и объединение в tuple

    Args:
        sql (str): sql запрос на выборку

    Returns:
        tuple: dicts in tuple
    """
    con = firebirdsql.connect(dsn=config.dsn,
                              user=config.user,
                              password=config.password,
                              charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    result = {}
    fieldIndices = range(len(cur.description))
    selectFields = ()
    for fieldDesc in cur.description:
        selectFields = *selectFields, fieldDesc[firebirdsql.DESCRIPTION_NAME]
    result2 = ()
    for row in cur:
        for fieldIndex in fieldIndices:
            result[selectFields[fieldIndex]] = row[fieldIndex]
        result2 = (*result2, result)
    cur.close()
    del cur
    return result2


def sel_dict_in_turple_desc(sql):
    """
    Формирование кортежа из словарей 
        вида ключ:значение, где ключ берется из название столбца в запросе
    Args:
        sql (str): sql для выборки
    Returns:
        tuple: dicts in tuple
    """
    con = firebirdsql.connect(dsn=config.dsn,
                              user=config.user,
                              password=config.password,
                              charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    select_fields = ()
    for field_desc in cur.description:
        select_fields = *select_fields, field_desc[firebirdsql.DESCRIPTION_NAME]
    dict_select = {}
    result_4 = []
    for row in cur:
        for i, _ in enumerate(select_fields):
            dict_select[select_fields[i]] = row[i]
        result_4.append(dict_select)
        dict_select = {}
    cur.close()
    del cur
    return result_4
