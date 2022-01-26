import fdb
import config


def select(sql):
    con = fdb.connect(dsn=config.dsn,
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
    con = fdb.connect(dsn=config.dsn,
                      user=config.user,
                      password=config.password,
                      charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


def proc(proc_name):
    con = fdb.connect(dsn=config.dsn,
                      user=config.user,
                      password=config.password,
                      charset=config.charset)
    cur = con.cursor()
    cur.callproc(proc_name)
    output_params = cur.fetchone()
    return output_params


def select_dicts_in_turple(sql):
    con = fdb.connect(dsn=config.dsn,
                      user=config.user,
                      password=config.password,
                      charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    result = {}
    fieldIndices = range(len(cur.description))
    selectFields = ()
    for fieldDesc in cur.description:
        selectFields = *selectFields, fieldDesc[fdb.DESCRIPTION_NAME]
    result2 = ()
    for row in cur:
        for fieldIndex in fieldIndices:
            result[selectFields[fieldIndex]] = row[fieldIndex]
        result2 = (*result2, result)
    cur.close()
    del cur
    return result2


def select_dicts_in_turple2(sql):
    con = fdb.connect(dsn=config.dsn,
                      user=config.user,
                      password=config.password,
                      charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    result = {}
    fieldIndices = range(len(cur.description))
    selectFields = ()
    for fieldDesc in cur.description:
        selectFields = *selectFields, fieldDesc[fdb.DESCRIPTION_NAME]
    result2 = ()
    for row in cur:
        for fieldIndex in fieldIndices:
            result[selectFields[fieldIndex]] = row[fieldIndex]
        result2 = (*result2, result)
    cur.close()
    del cur
    return result2
