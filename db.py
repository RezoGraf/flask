import fdb
import config


def select(sql):
    con = fdb.connect(dsn=config.dsn,
                      user=config.user, password=config.password, charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


def write(sql):
    con = fdb.connect(dsn=config.dsn,
                      user=config.user, password=config.password, charset=config.charset)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


def proc(proc_name):
    con = fdb.connect(dsn=config.dsn,
                      user=config.user, password=config.password, charset=config.charset)
    cur = con.cursor()
    cur.callproc(proc_name)
    output_params = cur.fetchone()
    return output_params
