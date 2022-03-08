SQL_INS_RSP_BLC = """INSERT INTO RSP_BLC (IBLC,DOC,DTN,DTK,RSN,TIP) 
                             VALUES({output_params},'{doc}','{InsDtn}','{InsDtk}','{InsRsn}',1)"""

SQL_DEL_RSP_BLC = """DELETE FROM RSP_BLC WHERE IBLC={DelIblc}"""

SQL_UPD_RSP_BLC = """UPDATE RSP_BLC SET dtn='{UpdDtn}', dtk='{UpdDtk}', rsn={UpdRsn} WHERE IBLC={UpdIblc}"""

SQL_UPD_IT_RASP_DUTY = """UPDATE IT_RASP_DUTY SET DATE_DUTY='{UpdDtnDuty}',ID_INTERVAL_TIME={UpdTimeDuty},NDAY={UpdNDay},DOC={doc},ROOM={UpdRoomDuty}
                          WHERE ID={UpdId} """

SQL_DEL_IT_RASP_DUTY = """DELETE FROM IT_RASP_DUTY WHERE ID={DelId} """

SQL_INS_IT_RASP = """INSERT INTO IT_RASP (LPU,OTD,SPZ,DOC,ROOM,NTV,ID_INTERVAL1,ID_INTERVAL2,NLIST)
                             VALUES({lpu},{otd},{spz},{doc},{room},{ntv},{interval1},{interval2},{nlist})"""

SQL_DEL_IT_RASP = """DELETE FROM IT_RASP WHERE DOC={doc} """
#обновление данных в графике работы время работы
sql_upd_it_rasp_grf = "UPDATE IT_RASP_GRF set {day_col}={day_zn} where id_grf={id_grf}"
#обновление данных в графике работы
sql_upd_it_rasp_grf_ = "UPDATE IT_RASP_GRF set {new_data} where id_grf={id_grf}"
#запись через интернет убираем
SQL_UPD_PSPO_S = """ UPDATE PSPO_S SET BLC=0 WHERE (UID=0) AND (BLC=1) 
                     AND UIP IN (SELECT DISTINCT UIP FROM PSPO WHERE PSPO.MPP={doc} 
                     AND (PSPO.DV>='{dtn}' AND PSPO.DV<='{dtk}'))"""        
# убираем СМС рассылки
SQL_DEL_SMS_SEND = """DELETE FROM SMS_SEND WHERE STATUS=0 and 
                        UIP IN (SELECT DISTINCT UIP FROM PSPO WHERE PSPO.MPP={doc} 
                        AND (PSPO.DV>='{dtn}' AND PSPO.DV<='{dtk}'))"""
# удалить запись из таблицы график работы
SQL_DELETE_GRF = """DELETE FROM IT_RASP_GRF WHERE ID_GRF={id_grf}"""