# coding=utf-8
from flask import Blueprint, g, session, render_template, request, redirect, url_for
from time import time
import numpy
from db_test.db_test_sql import sql_visit1, sql_visit2, sql_visit3
import app.db as db
from . import db_test
from app.menu_script import generate_menu


db_test = Blueprint('db_test', __name__)


@db_test.route('/', methods=['GET', 'POST'])
def main():
    list = []
    select_requests=[('Короткий, для теста скорости подключения', 1), ('Средний, для теста скорости подключения и выборки 10тыс+ записей', 2), ('Огромный, внимание очень тяжелый скрипт, не больше 2 раз',3)]
    select_counts = [('1',1), ('2',2), ('5',5), ('10',10), ('50',50), ('100',100), ('500',500), ('1тыс',1000), ('10тыс',10000)]
    
    if request.method == 'POST':
        script_select = request.form.get('script_select')
        count_select = request.form.get('count_select')
        return redirect(url_for('db_test.main',
                                nameid_selected=script_select,
                                countid_selected=count_select))
    else:
        sql_request= ""
        script_select = request.args.get('nameid_selected')
        count_select = request.args.get('countid_selected')
        if script_select is None:
            script_select = 1
        if count_select is None:
            count_select = 1
        if type(count_select) == str:
            count_select = int(count_select)
        if type(script_select) == str:
            script_select = int(script_select)
        if script_select == 1:
            sql_request = sql_visit1
        if script_select == 2:
            sql_request = sql_visit2
        if script_select == 3:
            sql_request = sql_visit3
        print(sql_request)

        a = []
        i = 0
        while i <= count_select:
            tic = time()
            test_select = db.select(sql_request)
            how_many = 0
            for key in test_select:
                how_many += 1
            print (how_many)
            toc = time()
            timeresult = (toc - tic)
            print(timeresult)
            i += 1
            a.append(timeresult)
        min_time = round(min(a), 3)
        average_time = round(numpy.average(a), 3)
        max_time = round(max(a), 3)
        if 'arena_fio' in session:
            arena_fio = session.get('arena_fio')
        else:
            arena_fio = "Не пользователь домена"
        menu = generate_menu()
        return render_template('db_test.html',
                            arena_fio=arena_fio,
                            min_time=min_time,
                            average_time=average_time,
                            max_time=max_time,
                            select_requests=select_requests,
                            select_counts=select_counts,
                            count_select=count_select,
                            script_select=script_select,
                            menu = menu
                            )
