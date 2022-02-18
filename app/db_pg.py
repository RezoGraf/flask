<<<<<<< HEAD:app/db_pg.py
import pg8000
=======
import psycopg2
>>>>>>> 62e56751d4d79069ba8e78c483dbda902f6c51fb:app/db-pg.py
import config
# import wtforms_sqlalchemy.orm.model_form


def select(sql):
<<<<<<< HEAD:app/db_pg.py
    con = pg8000.connect(host=config.pg_dsn, port=5432,
                             database='helios',
                             user=config.pg_user, password=config.pg_password)
=======
    con = psycopg2.connect(dsn=config.pg_dsn,
                        database = 'helios',
                        user=config.pg_user,
                        password=config.pg_password)
>>>>>>> 62e56751d4d79069ba8e78c483dbda902f6c51fb:app/db-pg.py
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


def write(sql):
<<<<<<< HEAD:app/db_pg.py
    con = pg8000.connect(host='192.168.100.52',
                             database='helios',
                             user='postgres', password='Gecnjq01!')
=======
    con = psycopg2.connect(dsn=config.pg_dsn,
                        database = 'helios',
                        user=config.pg_user,
                        password=config.pg_password)
>>>>>>> 62e56751d4d79069ba8e78c483dbda902f6c51fb:app/db-pg.py
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()
    del cur


def proc(proc_name):
<<<<<<< HEAD:app/db_pg.py
    con = pg8000.connect(host=config.pg_dsn, port=5432,
                             database='helios',
                             user=config.pg_user, password=config.pg_password)
=======
    con = psycopg2.connect(dsn=config.pg_dsn,
                        database = 'helios',
                        user=config.pg_user,
                        password=config.pg_password)
>>>>>>> 62e56751d4d79069ba8e78c483dbda902f6c51fb:app/db-pg.py
    cur = con.cursor()
    cur.callproc(proc_name)
    output_params = cur.fetchone()
    con.commit()
    return output_params

# Base = automap_base()

# engine = create_engine("postgresql+pg8000://postgres:Gecnjq01!@192.168.100.52/helios", client_encoding='utf8')
# Base.prepare(engine, reflect=True)
# Worker = Base.classes.epid_Worker
# print(Worker)
# session = Session(engine)
# results = Base.session.query(Worker).all()
#     for r in results:
#         print(r.IDW)


# db = SQLAlchemy(app)

# # worker = db.Table('epid_Worker', db.metadata, autoload=True, autoload_with=db.engine)
# # session.add(Address(email_address="foo@bar.com", user=User(name="foo")))
# session.commit()

# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
# Worker = Base.classes.epid_Worker

# @app.route('/')
# def index():
#     # db.session.query(worker).all()
#     # worker.session.all()
#     results = db.session.query(Worker).all()
#     for r in results:
#         print(r.IDW)
#     return ''

# if __name__ == "__main__":
#     # app.run(host='192.168.100.142', port=80, debug=True)
#     app.run(host='0.0.0.0', port=4000)
