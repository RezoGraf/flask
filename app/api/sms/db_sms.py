"""Функции для работы с бд Firebird"""
import firebirdsql
import config_sms


def select(sql):
    """Выборка из бд firebird

    Args:
        sql (str): sql запрос на выборку

    Returns:
        tuple: tuple с list внутри
    """
    con = firebirdsql.connect(dsn=config_sms.dsn,
                              user=config_sms.user,
                              password=config_sms.password,
                              charset=config_sms.charset)
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
    con = firebirdsql.connect(dsn=config_sms.dsn,
                              user=config_sms.user,
                              password=config_sms.password,
                              charset=config_sms.charset)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur
