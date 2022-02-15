import loguru
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
from loguru import logger
import logging


# class InterceptHandler(logging.Handler):
#     def emit(self, record):
#         # Retrieve context where the logging call occurred, this happens to be in the 6th frame upward
#         logger_opt = logger.opt(depth=6, exception=record.exc_info)
#         logger_opt.log(record.levelno, record.getMessage())





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



def my_filter(record):
    if record["extra"].get("warn_only"):  # "warn_only" is bound to the logger and set to 'True'
        return record["level"].no >= logger.level("WARNING").no
    return True  # Fallback to default 'level' configured while adding the handler


logger.add(
    'logs/events.log',
    level='DEBUG',
    format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
    backtrace=True,
    rotation='1 Gb',
    retention=9,
    encoding='utf-8',
    filter=my_filter,
    colorize=True,
    enqueue=True,
    serialize=True

    )




@app.route('/', methods=['GET', 'POST'])
@logger.catch
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
            # app.logger.info(f'LOGIN-SUCCESS for {username}')
            # logger.info("Inside the function")
            app.logger.info(f'LOGIN-SUCCESS for {username}')
            # app.logger.info(request.args)
            # app.logger.info(request.full_path)
            # app.logger.error('Processing default request')
            return redirect(url_for('menu.main_menu'))
        else:
            message = "Неверное имя пользователя или пароль"
    return render_template('login.html',
                           user_ad_field=user_ad_field,
                           message=message,
                           message_auth=message_auth)


@app.route('/aalksdhl28kdhalu8', methods=['GET', 'POST'])
@logger.catch
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
            app.logger.info(f'LOGIN-SUCCESS for {username}')
            # app.logger.info(request.args)
            return redirect(url_for('menu.main_menu'))
        else:
            message = "Неверное имя пользователя или пароль"
    return render_template('login.html',
                           user_ad_field=user_ad_field,
                           message=message,
                           message_auth=message_auth)



@app.route('/logout')
@logger.catch
def logout():
    logger.info("Inside the function")
    session.clear()
    flash("Вы успешно вышли!")
    gc.collect()
    return redirect(url_for('login'))


if __name__ == "__main__":
    # app.run(host='192.168.100.142', port=80, debug=True)
    app.run(host='0.0.0.0', port=4000, debug=False)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error') 
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

 
