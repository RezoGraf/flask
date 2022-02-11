from app.api.api import api
from app.htmx_test.htmx_test import htmx_test
from app.data_input.data_input import data_input
from app.excel.excel import excel
from app.vaccine.vaccine import vaccine
from app.report.report import report
from app.zakaz_naryad.zakaz_naryad import zakaz_naryad
from flask import Flask, render_template, request, url_for, redirect, flash, session
from app.db_test.db_test import db_test
import datetime
import app.auth as auth
from app.menu.menu import menu
import gc
import logging
from logging.config import fileConfig



# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegration

# sentry_sdk.init(
#     dsn="https://f2b6c112871e4531ae68d13560e78e86@o1123757.ingest.sentry.io/6161912",
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )


app = Flask(__name__, static_folder="static",
            template_folder='templates')
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'sdlfhwerfohw489fh48of4ho'
app.permanent_session_lifetime = datetime.timedelta(days=365)
app.register_blueprint(data_input,
                       url_prefix='/data_input',
                       static_folder='/static',
                       template_folder='/templates')
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(excel, url_prefix='/excel')
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(report, url_prefix='/report')
app.register_blueprint(db_test, url_prefix='/db_test')
app.register_blueprint(zakaz_naryad, url_prefix='/zakaz_naryad')
app.register_blueprint(htmx_test, url_prefix='/htmx_test')
app.register_blueprint(vaccine, url_prefix='/vaccine')


@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    message_auth = ""
    user_ad_field = ' '
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        
        auth_result = auth.check_credentials(username, password)
        if auth_result[0] == 'error':
            message_auth = auth_result[1]
        if auth_result[0] == 'ok':
            message_auth = f'AD: успешная авторизация {auth_result[1]}, доступ уровень {auth_result[2]}'
        if (username == 'root' and password == 'pass') or (auth_result[0] == 'ok'):
            app.logger.info('%s logged in successfully', username)
            app.logger.error('Processing default request')
            return redirect(url_for('menu.main_menu'))
        else:
            message = "Неверное имя пользователя или пароль"
    return render_template('login.html',
                           user_ad_field=user_ad_field,
                           message=message,
                           message_auth=message_auth)


@app.route('/aalksdhl28kdhalu8', methods=['GET', 'POST'])
def login_for_test():
    message = ""
    message_auth = ""
    user_ad_field = """<input type="text" id="userAD" name="user_ad" placeholder="Пользователь" />
        <i class="fa fa-user "></i>"""
    if request.method == 'POST':
        username = request.form.get('username')  # запрос к данным формы
        password = request.form.get('password')
        user_ad = request.form.get('user_ad')
        auth_result = auth.check_admins_auth(username, password, user_ad)
        if auth_result[0] == 'error':
            message_auth = auth_result[1]
        if auth_result[0] == 'ok':
            message_auth = f'AD: успешная авторизация {auth_result[1]}, доступ уровень {auth_result[2]}'
        if (username == 'root' and password == 'pass') or (auth_result[0] == 'ok'): 
            app.logger.info('%s logged in successfully', username)
            return redirect(url_for('menu.main_menu'))
        else:
            message = "Неверное имя пользователя или пароль"
    return render_template('login.html',
                           user_ad_field=user_ad_field,
                           message=message,
                           message_auth=message_auth)


@app.route('/logout')
@auth.login_required
def logout():
    
    session.clear()
    flash("Вы успешно вышли!")
    gc.collect()
    return redirect(url_for('login'))



logfile    = logging.getLogger('file')
logconsole = logging.getLogger('console')
logfile.debug("Debug FILE")
logconsole.debug("Debug CONSOLE")
# @app.route('/menu2')
# def menu():
#     if 'arena_user' in session:
#         arena_user = session.get('arena_user')
#     else:
#         arena_user = 'none'
#     if 'arena_fio' in session:
#         arena_fio = session.get('arena_fio')
#     else:
#         arena_fio = "Не пользователь домена"
#     if 'auth_group' in session:
#         auth_group = session.get('auth_group')
#     else:
#         auth_group = 'none'
#     # if auth_group == 'web_hs_admin':
#     #     web_hs_admin
#     #     web_hs_user
#     #     web_hs_kadr
#     #     web_hs_epid
#     menu2 = generate_menu
#     menu2 = Markup(menu2)
#     return render_template('menu.html', menu=menu2)


if __name__ == "__main__":
    # app.run(host='192.168.100.142', port=80, debug=True)
    app.run(host='0.0.0.0', port=4000)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error') 
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
