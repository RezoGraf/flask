"""Функции для работы с БД Postgresql"""
import psycopg2
from config import (pg_database, pg_user, pg_dsn, pg_port, pg_password)


dsn = f'dbname={pg_database} user={pg_user} host={pg_dsn} port={pg_port} password={pg_password}'


def select(sql):
    """Выборка из бд firebird

    Args:
        sql (str): строка sql запроса

    Returns:
        _type_: _description_
    """
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


def write(sql):
    """Записать данные в бд firebird

    Args:
        sql (str): строка sql запроса
    """
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


def proc(proc_name):
    """Выполнить процедуру и вернуть номер для id записи

    Args:
        proc_name (str): вызов процедуры

    Returns:
        tuple: возвращает tuple от выполнения процедуры
    """    
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.callproc(proc_name)
    output_params = cur.fetchone()
    con.commit()
    return output_params


def select_dicts_in_list_with_description(sql) -> list:
    """Выборка в словари вида название столбца:значение в списке

    Args:
        sql (str): строка sql запроса на выборку данных из бд pg

    Returns:
        list: Список со словарями, где ключи - название колонок
    """
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.execute(sql)
    columns = list(cur.description)
    result = cur.fetchall()
    results = []
    for row in result:
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col.name] = row[i]
            results.append(row_dict)
    return results