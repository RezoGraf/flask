import firebirdsql
import config
import utils
from collections import defaultdict


def select(sql):
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
                color_ = utils.date_color(dc)
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
