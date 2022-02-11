
# Запрос на проверку документа

sql_prov = "SELECT idkv,stu FROM pl_uslk WHERE idkv={doc_id}"

# Проверка суммы. 1. Сумма (STU) из запроса=Сумма DOC_SUM из JSON все ОК. Запрос на обновление информации
sql_api_upd = """UPDATE PL_USLK 
                    SET STATUS=2, SNAL={DOC_SUM_NAL}, SPLK={DOC_SUM_BNAL}, KAS={KAS_KOD}, CHECK_TYPE=1, CHECK_NUM={DOC_NOM}, 
                    KSKID=0"""

# Если {DOC_TYPE_OPL}=4, то обновить поле   KOM=KOM||{DOC_SUM_RAS}||{DOC_DATE}    KOM=KOM+{DOC_SUM_RAS}+{DOC_DATE}
sql_api_upd2 = """UPDATE PL_USLK
                    SET STATUS=2, SNAL={doc_sum_nal}, SPLK={doc_sum_bnal}, KAS={kas_kod}, CHECK_TYPE=1, CHECK_NUM={doc_nom}, DRED='{dred}',
                    KSKID={doc_type_opl}{kom} WHERE IDKV={doc_id}"""

# 2. Сумма (STU) из запроса<>Сумма DOC_SUM из JSON, то запрос
sql_api_ins = """INSERT INTO PL_USLK_EXP (IDKV,ERR,DATE_EXP,JSON_,JSON_OTV) 
                  VALUES ({doc_id}, {kod_err}, '{now_date}', '{json1}', '{res_proverki}')"""