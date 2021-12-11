import fdb
import config


def db_select(sql):
    con = fdb.connect(dsn=config.DB_CONFIG,
                      user=config.DB_USER, password=config.DB_PASSWORD, charset=config.DB_CHARSET)
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


def db_write(sql):
    con = fdb.connect(dsn=config.DB_CONFIG,
                      user=config.DB_USER, password=config.DB_PASSWORD, charset=config.DB_CHARSET)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


def db_proc(proc_name):
    con = fdb.connect(dsn=config.DB_CONFIG,
                      user=config.DB_USER, password=config.DB_PASSWORD, charset=config.DB_CHARSET)
    cur = con.cursor()
    cur.callproc(proc_name)
    output_params = cur.fetchone()
    return output_params
