sql_ins_rsp_blc = """INSERT INTO RSP_BLC (IBLC,DOC,DTN,DTK,RSN,TIP) 
                             VALUES({output_params},'{doc}','{InsDtn}','{InsDtk}','{InsRsn}',1)"""

sql_del_rsp_blc = """DELETE FROM RSP_BLC WHERE IBLC={DelIblc}"""

sql_upd_rsp_blc = """UPDATE RSP_BLC SET dtn='{UpdDtn}', dtk='{UpdDtk}', rsn='{UpdRsn}' WHERE IBLC={UpdIblc}"""