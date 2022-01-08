sql_ins_rsp_blc = """INSERT INTO RSP_BLC (IBLC,DOC,DTN,DTK,RSN,TIP) 
                             VALUES({output_params},'{doc}','{InsDtn}','{InsDtk}','{InsRsn}',1)"""

sql_del_rsp_blc = """DELETE FROM RSP_BLC WHERE IBLC={DelIblc}"""

sql_upd_rsp_blc = """UPDATE RSP_BLC SET dtn='{UpdDtn}', dtk='{UpdDtk}', rsn={UpdRsn} WHERE IBLC={UpdIblc}"""

sql_ins_it_rasp_duty = """INSERT INTO IT_RASP_DUTY (ID,DOC,DATE_DUTY,ID_INTERVAL_TIME,NDAY) 
                             VALUES({output_params},{doc},'{InsDtnDuty}',{InsTimeDuty},{InsNDay})"""

sql_upd_it_rasp_duty = """UPDATE IT_RASP_DUTY SET DATE_DUTY='{UpdDtnDuty}',ID_INTERVAL_TIME={UpdTimeDuty},NDAY={UpdNDay}
                          WHERE ID={UpdId} """

sql_del_it_rasp_duty = """DELETE FROM IT_RASP_DUTY WHERE ID={DelId} """

sql_ins_it_rasp = """INSERT INTO IT_RASP (LPU,OTD,SPZ,DOC,ROOM,NTV,ID_INTERVAL1,ID_INTERVAL2,NLIST) 
                             VALUES({lpu},{otd},{spz},{doc},{room},{ntv},{interval1},{interval2},{nlist})"""

sql_del_it_rasp = """DELETE FROM IT_RASP WHERE DOC={doc} """

