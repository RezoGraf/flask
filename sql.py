# Выборка для отчета
sql_select = """SELECT  (
SELECT  SNLPU
FROM N_LPU
WHERE N_DOC.LPU=N_LPU.LPU
AND N_LPU.TER=5), (select nmpp from n_mpp where n_mpp.mpp=n_doc.mpp) as NDOC, (
SELECT  NRSN
FROM RSP_RSN
WHERE RSP_RSN.RSN=RSP_BLC.RSN), RSP_BLC.DTN , RSP_BLC.DTK
FROM RSP_BLC, N_DOC
WHERE (RSP_BLC.DOC=N_DOC.DOC)
AND (RSP_BLC.DTK>='{dtn}' AND RSP_BLC.DTK<='{dtk}')"""

# Выбор списка отделений
sql_allOtd = "select otd,notd from np_otd where notd is not null order by ps"
# Выбор текущего отделения
sql_currentOtd = "select otd, notd, lpu from np_otd where otd='{otd}'"
# Выборка первого попавшегося отделения
sql_randomOtd = """select first 1 otd from np_otd where otd>0 order by otd"""

# Выборка всех ФИО врачей по коду отделения
sql_allDoc = """select n_doc.doc, n_doc.ndoc||' ('||n_dlj.ndlj||')' as ndoc from n_doc, n_dlj where (n_doc.dolj=n_dlj.dlj) and n_doc.pv=1 and n_doc.otd='{otd}' order by ndoc """
# Выборка первого попавшегося врача
sql_randomDoc = """select first 1 doc from n_doc where pv=1 and otd='{otd}' order by ndoc"""
# Выборка ФИО по коду
sql_fio_sotrudnika = """select distinct n_mpp.nmpp from n_doc, n_mpp where (n_doc.mpp=n_mpp.mpp) and n_doc.doc={doc} """

# Причина отсутствия на рабочем месте
sql_rsp_rsn = """select rsn, nrsn from rsp_rsn order by rsn"""

# Номера кабинетов
sql_room = """select id, nroom_kr from room where lpu in (select distinct lpu from n_doc where doc={doc}) order by id"""

# Выборка всех специальностей сотрудников
sql_allSpz = """select spz, nspz from n_spz where pd=1 order by nspz"""

# Информация о режиме работы сотрудника
sql_it_rasp = """Select ROOM.NROOM_KR,(select interval_time from it_rasp_time where it_rasp_time.id=it_rasp.ID_INTERVAL1) as NOEVEN_DAY,
                 (select interval_time from it_rasp_time where it_rasp_time.id=it_rasp.ID_INTERVAL1) as EVEN_DAY,IT_RASP.NTV,IT_RASP.NLIST,N_SPZ.NSPZ 
                 from IT_RASP,ROOM,N_SPZ 
                 where (it_rasp.room=room.id) and (it_rasp.spz=n_spz.spz) and doc='{doc}'"""

# Информация об отсутствии на работе
sql_noWork = """Select iblc, CAST (dtn AS date), CAST (dtk AS date), (select nrsn from rsp_rsn where rsp_rsn.rsn=rsp_blc.rsn) as nrsn_ 
                from rsp_blc where doc='{doc}' order by dtn desc"""

# Информация о дежурстве
sql_it_rasp_duty = """Select ID,DATE_DUTY, 
                 (select interval_time from it_rasp_time where it_rasp_time.id=IT_RASP_DUTY.ID_INTERVAL_TIME) as TIME_DUTY,
                 CASE EXTRACT (WEEKDAY FROM date_duty)  
                     WHEN 1 THEN 'Понедельник'
                     WHEN 2 THEN 'Вторник'
                     WHEN 3 THEN 'Среда'
                     WHEN 4 THEN 'Четверг'
                     WHEN 5 THEN 'Пятница'
                     WHEN 6 THEN 'Суббота'
                     WHEN 0 THEN 'Воскресенье'
                 END as denNedeli
                 from IT_RASP_DUTY 
                 where doc='{doc}' order by DATE_DUTY"""

# Время работы
sql_interval_time = """select id, interval_time from it_rasp_time order by id"""

sql_doctod = """ select doc, ndoc from n_doc where pv=1 and doc='{doc}' and otd='{otd}'"""

sql_otd_for_report = """"""
