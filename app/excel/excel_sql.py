# sql_select_otsut = """Select N_DOC.NDOC, (SELECT SNLPU FROM N_LPU WHERE N_DOC.LPU=N_LPU.LPU and N_LPU.TER=5),
#     (SELECT NRSN FROM RSP_RSN WHERE RSP_RSN.RSN=RSP_BLC.RSN),RSP_BLC.DTN ,RSP_BLC.DTK
# from RSP_BLC,N_DOC
# where (RSP_BLC.DOC=N_DOC.DOC) and ((RSP_BLC.DTK>='{date_start}'
#     and RSP_BLC.DTK<='{date_finish}') or (RSP_BLC.DTN>='{date_start}' and RSP_BLC.DTN<='{date_finish}'))"""