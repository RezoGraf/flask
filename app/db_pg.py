import psycopg2
import config
# import wtforms_sqlalchemy.orm.model_form
dsn = f'dbname={config.pg_database} user={config.pg_user} host={config.pg_dsn} port={config.pg_port} password={config.pg_password}'

def select(sql):
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


def write(sql):
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


def proc(proc_name):
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.callproc(proc_name)
    output_params = cur.fetchone()
    con.commit()
    return output_params


def select_dicts_in_turple_with_description(sql):
    con = psycopg2.connect(dsn)
    cur = con.cursor()
    cur.execute(sql)
    selectFields = ()
    for fieldDesc in cur.description:
        selectFields = *selectFields, fieldDesc[psycopg2.DESCRIPTION_NAME]
    dict_select = {}
    result_4 = []
    for row in cur:
        for i in range(len(selectFields)):
            dict_select[selectFields[i]] = row[i]
        # result_4 += dict_select
        result_4.append(dict_select)
        dict_select = {}
    cur.close()
    del cur
    return result_4