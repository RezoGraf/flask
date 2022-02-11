from flask import Blueprint, Flask, jsonify, request
import app.db as db
import datetime
import json
from app.api.sql_api import sql_prov, sql_api_ins, sql_api_upd2

api = Blueprint('api', __name__)

@api.route('/oplata_1c', methods=['POST'])
def oplata_1c():

    dict = request.json
    json_for_table = request.json
    usr = request.args.get('Usr')
    pwd = request.args.get('Pwd')
    usr_true = 'web_helix'
    pwd_true = '111'
    key_true = "DOC"
    list_str = json.dumps(json_for_table)
    key_json = list(dict.keys())[0]
    if key_json == key_true:
        if usr == usr_true and pwd == pwd_true:
            #               0               1           2             3               4              5                   6               7               8           9
            key_chek = (" DOC_ID ",	" DOC_DATE ", " DOC_NOM ", " DOC_TYPE_OPL ", " DOC_SUM ", " DOC_SUM_NAL ",	" DOC_SUM_BNAL ", " DOC_SUM_RAS ", " CHECK_NUM ", " KAS_KOD ")
            key_model = list(key_chek)
            status = ([])
            otvet_list = ([])
            for firstkey, big_list in dict.items():
                for i, pair in enumerate(big_list):
                    keys = list(pair.keys())
                    list_result = ([])
                    res = [x for x in key_model + keys if x not in key_model or x not in keys]

                    if not res:

                        status.append(f"{i} - Структура соответствует")

                        for i in range(0, len(pair)):

                            list_result.append(pair[key_model[i]])

                    else:

                        status.append(f"{i} - Структура НЕ соответствует по ячейкам {res} у массива: {str(pair)}")
                print(i)
                otvet_list.append(list_result)
                print(list_result[0])
                res_sql_prov = db.select(sql_prov.format(doc_id=list_result[0]))
                print(res_sql_prov)
                now_date = datetime.datetime.now()
                now_date = now_date.strftime('%Y.%m.%d %H:%M:%S')
                if res_sql_prov:
                    for vol in res_sql_prov:
                        vol = list(vol)
                # Сумма (STU) из запроса<>Сумма DOC_SUM из JSON, то запрос -----------------------------

                        if vol[1] != float(list_result[4]):

                            

                            # print(sql_api_ins.format(doc_id=list_result[0], kod_err=20, now_date=now_date, json1=list_str,
                            #                         res_proverki='Не совпадает сумма'))
                            db.write(sql_api_ins.format(doc_id=list_result[0], kod_err=20, now_date=now_date,
                                                        json1=list_str, res_proverki='Не совпадает сумма'))

                        if int(list_result[3]) == 4:
                            kom = f""", KOM=KOM||'{list_result[7]}, {list_result[1]}/'"""

                            # print(sql_api_upd2.format(doc_sum_nal=list_result[5],
                            #                         doc_sum_bnal=list_result[6], kas_kod=list_result[9],
                            #                         doc_nom=list_result[2], doc_type_opl=4, dred=now_date, kom=kom,
                            #                         doc_id=list_result[0]))
                            db.write(sql_api_upd2.format(doc_sum_nal=list_result[5],
                                                    doc_sum_bnal=list_result[6], kas_kod=list_result[9],
                                                    doc_nom=list_result[2], doc_type_opl=4, dred=now_date, kom=kom,
                                                    doc_id=list_result[0]))
                            db.write(sql_api_ins.format(doc_id=list_result[0], kod_err=0, now_date=now_date,
                                                        json1=list_str, res_proverki='ОК'))
                        else:

                            # print(sql_api_upd2.format(doc_sum_nal=list_result[5],
                            #                         doc_sum_bnal=list_result[6], kas_kod=list_result[9],
                            #                         doc_nom=list_result[2], doc_type_opl=0, kom='', dred=now_date,
                            #                         doc_id=list_result[0]))
                            
                            db.write(sql_api_upd2.format(doc_sum_nal=list_result[5],
                                                    doc_sum_bnal=list_result[6], kas_kod=list_result[9],
                                                    doc_nom=list_result[2], doc_type_opl=0, dred=now_date, kom='',
                                                    doc_id=list_result[0]))
                            db.write(sql_api_ins.format(doc_id=list_result[0], kod_err=0, now_date=now_date,
                                                        json1=list_str, res_proverki='ОК'))
                    
                else:
                    list_str = json.dumps(json_for_table)
                    db.write(sql_api_ins.format(doc_id=list_result[0], kod_err=20, now_date=now_date,
                                                        json1=list_str, res_proverki='Документ не найден'))
                    # return "Документ не найден", 200
                    status.append(f"{list_result[0]} - Документ не найден")    
                return (f"Status = {status}, DataADD: {otvet_list}")
        else:
            return 'Неверынй логин пароль', 401
    else:
        return 'Неверный заголовок JSON, должен быть "DOC"', 400


@api.route('/test_api', methods=['GET', 'POST'])
def test_api():
    json = request.json
    return json