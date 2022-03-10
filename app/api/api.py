from flask import Blueprint, Flask, jsonify, request
import app.db as db
import datetime
from loguru import logger
import logging
import json
from app.api.sql_api import sql_prov, sql_api_ins, sql_api_upd2
import requests
import app.sql as sql
import re 
api = Blueprint('api', __name__)


@api.route('/oplata_1c', methods=['POST'])
@logger.catch
def oplata_1c():
    """_summary_

    Returns:
        _type_: _description_
    """
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
            #               0           1           2             3           4              5
            key_chek = ("DOC_ID",	"DOC_DATE", "DOC_NOM", "DOC_TYPE_OPL", "DOC_SUM", "DOC_SUM_NAL",
                        #6               7              8            9
                        "DOC_SUM_BNAL", "DOC_SUM_RAS", "CHECK_NUM", "KAS_KOD")
            key_model = list(key_chek)
            status = ([])
            otvet_list = ([])
            for _, big_list in dict.items():
                for i, pair in enumerate(big_list):
                    keys = list(pair.keys())
                    list_result = ([])
                    res = [x for x in key_model + keys if x not in key_model or x not in keys]
                    if res:
                        status.append(f"{i} - Структура НЕ соответствует по ячейкам {res} у массива: {str(pair)}")
                    else:
                        status.append(f"{i} - Структура соответствует")
                        for i in range(0, len(pair)):
                            list_result.append(pair[key_model[i]])
                        otvet_list.append(list_result)
                        res_sql_prov = db.select(sql_prov.format(doc_id=list_result[0]))
                        now_date = datetime.datetime.now()
                        now_date = now_date.strftime('%Y.%m.%d %H:%M:%S')
                        if res_sql_prov:
                            for vol in res_sql_prov:
                                vol = list(vol)
                        # Сумма (STU) из запроса<>Сумма DOC_SUM из JSON, то запрос -----------------------------
                                if vol[1] != float(list_result[4]):
                                    db.write(sql_api_ins.format(doc_id=list_result[0], kod_err=20, now_date=now_date,
                                                                json1=list_str, res_proverki='Не совпадает сумма'))

                                if int(list_result[3]) == 4:
                                    kom = f""", KOM=KOM||'{list_result[7]}, {list_result[1]}/'"""
                                    db.write(sql_api_upd2.format(doc_sum_nal=list_result[5],
                                                            doc_sum_bnal=list_result[6], kas_kod=list_result[9],
                                                            doc_nom=list_result[2], doc_type_opl=4, dred=now_date, kom=kom,
                                                            doc_id=list_result[0]))
                                    db.write(sql_api_ins.format(doc_id=list_result[0], kod_err=0, now_date=now_date,
                                                                json1=list_str, res_proverki='ОК'))
                                else:
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
@logger.catch
def test_api():
    """_summary_

    Returns:
        _type_: _description_
    """
    json = request.json
    return json

# @api.route('/zn_close', methods=['GET', 'POST'])
@logger.catch
def zn_close():
    """_summary_

    Args:
        idkv (_type_): _description_

    Returns:
        _type_: _description_
    """
    url = 'http://127.0.0.1:5000/api/test_api'
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}
    # поиск документов на отправку со статусом 3-------
    result = db.sel_dict_in_turple_desc(sql.sql_api_select_check)
    # print(result)
    data = {}
    volue = []
    for i, _ in enumerate(result):
        dzr = result[i]['DZR']
        if dzr is not None:
            dzr = dzr.strftime('%d.%m.%Y')
            result_isp = db.sel_dict_in_turple_desc(sql.sql_api_select_isp.format(idkv=result[i]['IDKV']))
            te = result_isp[0]
            # print(te)
            val = list(te.values())
            # print(val)
            list_isp = []
            # Техник
            if val[0] != ("0", 0,  None):
                isp_vol = {"ISP_STAT":"5",
                           "ISP_CODE":str(val[0])}
                list_isp.append(isp_vol)
            # Литейщик
            if val[1] != ("0", 0,  None):
                isp_vol = {"ISP_STAT":"6",
                           "ISP_CODE":str(val[1])}
                list_isp.append(isp_vol)
            # Полир
            if val[2] != ("0", 0,  None):
                isp_vol = {"ISP_STAT":"7",
                           "ISP_CODE":str(val[2])}
                list_isp.append(isp_vol)
            # print(list_isp)
            data_vol = {"DOC_ID":str(result[i]['IDKV']),
                        "DOC_TYPE":"3",
                        "DOC_DZR":dzr,
                        "DOC_OPL":str(result[i]['OPL']),
                        "ISP":list_isp}
            volue.append(data_vol)
    data["DOC"] = volue
    answer = requests.post(url, data=json.dumps(data), headers=headers)
    response = answer.json()
    date_now = datetime.datetime.now()
    err = str(answer.status_code)
    date_otpr = date_now.strftime("%d.%m.%Y-%H:%M:%S")
    json_str = json.dumps(response)
    if answer.status_code in range(200, 300):
        # a = data['DOC']
        for _, doc_id in enumerate(data['DOC']):
            idkv = doc_id['DOC_ID']
            
        # print(data['DOC']['DOC_ID'])
            print(sql.sql_api_insert_log.format(idkv=idkv , err=err, date=date_otpr, json=json_str, json_otv=1))
        # print(answer.status_code)
    else:
        print("Не то пальто")
        print(answer.status_code)
    
    # print(response)
    return response