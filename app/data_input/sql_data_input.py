sql_ins_rsp_blc = """INSERT INTO RSP_BLC (IBLC,DOC,DTN,DTK,RSN,TIP) 
                             VALUES({output_params},'{doc}','{InsDtn}','{InsDtk}','{InsRsn}',1)"""

sql_del_rsp_blc = """DELETE FROM RSP_BLC WHERE IBLC={DelIblc}"""

sql_upd_rsp_blc = """UPDATE RSP_BLC SET dtn='{UpdDtn}', dtk='{UpdDtk}', rsn={UpdRsn} WHERE IBLC={UpdIblc}"""

sql_ins_it_rasp_duty = """INSERT INTO IT_RASP_DUTY (ID,DOC,DATE_DUTY,ID_INTERVAL_TIME,NDAY) 
                             VALUES({output_params},{doc},'{InsDtnDuty}',{InsTimeDuty},{InsNDay})"""

sql_upd_it_rasp_duty = """UPDATE IT_RASP_DUTY SET DATE_DUTY='{UpdDtnDuty}',ID_INTERVAL_TIME={UpdTimeDuty},NDAY={UpdNDay},DOC={doc},ROOM={UpdRoomDuty}
                          WHERE ID={UpdId} """

sql_del_it_rasp_duty = """DELETE FROM IT_RASP_DUTY WHERE ID={DelId} """

sql_ins_it_rasp = """INSERT INTO IT_RASP (LPU,OTD,SPZ,DOC,ROOM,NTV,ID_INTERVAL1,ID_INTERVAL2,NLIST) 
                             VALUES({lpu},{otd},{spz},{doc},{room},{ntv},{interval1},{interval2},{nlist})"""

sql_del_it_rasp = """DELETE FROM IT_RASP WHERE DOC={doc} """
#обновление данных в графике работы время работы
sql_upd_it_rasp_grf = "UPDATE IT_RASP_GRF set {day_col}={day_zn} where id_grf={id_grf}"
#обновление данных в графике работы
sql_upd_it_rasp_grf_ = "UPDATE IT_RASP_GRF set {new_data} where id_grf={id_grf}"
#запись через интернет убираем
sql_upd_pspo_s = """ UPDATE PSPO_S SET BLC=0 WHERE (UID=0) AND (BLC=1) 
                     AND UIP IN (SELECT DISTINCT UIP FROM PSPO WHERE PSPO.MPP={doc} 
                     AND (PSPO.DV>='{dtn}' AND PSPO.DV<='{dtk}'))"""        
# убираем СМС рассылки
sql_del_sms_send = """DELETE FROM SMS_SEND WHERE STATUS=0 and 
                        UIP IN (SELECT DISTINCT UIP FROM PSPO WHERE PSPO.MPP={doc} 
                        AND (PSPO.DV>='{dtn}' AND PSPO.DV<='{dtk}'))"""