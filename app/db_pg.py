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


def select_dicts_in_list_with_description(sql):
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