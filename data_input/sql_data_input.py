sql_ins_rsp_blc = """INSERT INTO RSP_BLC (IBLC,DOC,DTN,DTK,RSN,TIP) 
                             VALUES({output_params},'{doc}','{dtn}','{dtk}','{rsn}',1)"""

sql_del_rsp_blc = """DELETE FROM RSP_BLC WHERE IBLC={DelIblc}"""