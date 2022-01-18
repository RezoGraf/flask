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

# zakaz_naryad-----ВСЕ----------if check_open and check_close----------------------------------------------------
sql_zakaz_naryad_select = """Select pl_uslk.idkv,pl_uslk.nkv,pl_uslk.dou,pl_uslk.stu,pl_uslk.dzr, 
       n_opl.nopl,patient.uid,patient.fam,patient.im,patient.ot,patient.dr,
       (select nmpp from n_mpp where n_mpp.mpp=pl_uslk.vr) as nmpp,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.teh) as nteh,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.lit) as nlit,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.polir) as npolir,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.varh) as nvarh,
       (select distinct n_lpu.snlpu from n_slp,n_lpu where n_slp.slp=n_lpu.lpu and n_slp.ter=n_lpu.ter and n_slp.slp=pl_uslk.lpu) as nlpu
from pl_uslk,patient,np_otd,n_opl
Where (pl_uslk.uid=patient.uid) and (pl_uslk.otd=np_otd.otd) and (pl_uslk.opl=n_opl.opl)
  and (np_otd.GR_OTD=2) 
  and (pl_uslk.dou>='{dtn}' and pl_uslk.dou<='{dtk}')
order by idkv,dou"""
# Только открытые наряды------if check_open and check_close is None--------------------------------------------------------
sql_zakaz_naryad_select_open = """Select pl_uslk.idkv,pl_uslk.nkv,pl_uslk.dou,pl_uslk.stu,pl_uslk.dzr, 
       n_opl.nopl,patient.uid,patient.fam,patient.im,patient.ot,patient.dr,
       (select nmpp from n_mpp where n_mpp.mpp=pl_uslk.vr) as nmpp,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.teh) as nteh,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.lit) as nlit,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.polir) as npolir,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.varh) as nvarh,
       (select distinct n_lpu.snlpu from n_slp,n_lpu where n_slp.slp=n_lpu.lpu and n_slp.ter=n_lpu.ter and n_slp.slp=pl_uslk.lpu) as nlpu
from pl_uslk,patient,np_otd,n_opl
Where (pl_uslk.uid=patient.uid) and (pl_uslk.otd=np_otd.otd) and (pl_uslk.opl=n_opl.opl)
  and (np_otd.GR_OTD=2) 
  and (pl_uslk.dou>='{dtn}' and pl_uslk.dou<='{dtk}')
  and (pl_uslk.dzr is null)
order by idkv,dou"""
# Только закрытые наряды-------if check_open is None and check_close-------------------------------------------------------
sql_zakaz_naryad_select_close = """Select pl_uslk.idkv,pl_uslk.nkv,pl_uslk.dou,pl_uslk.stu,pl_uslk.dzr, 
       n_opl.nopl,patient.uid,patient.fam,patient.im,patient.ot,patient.dr,
       (select nmpp from n_mpp where n_mpp.mpp=pl_uslk.vr) as nmpp,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.teh) as nteh,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.lit) as nlit,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.polir) as npolir,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.varh) as nvarh,
       (select distinct n_lpu.snlpu from n_slp,n_lpu where n_slp.slp=n_lpu.lpu and n_slp.ter=n_lpu.ter and n_slp.slp=pl_uslk.lpu) as nlpu
from pl_uslk,patient,np_otd,n_opl
Where (pl_uslk.uid=patient.uid) and (pl_uslk.otd=np_otd.otd) and (pl_uslk.opl=n_opl.opl)
  and (np_otd.GR_OTD=2) 
  and (pl_uslk.dou>='{dtn}' and pl_uslk.dou<='{dtk}')
  and (pl_uslk.dzr is not null)
order by idkv,dou"""
# данные наряда по номеру------------------------------------------------------------------------------------------------
sql_zn_naryad_select_info = """Select pl_uslk.idkv,pl_uslk.nkv,pl_uslk.dou,pl_uslk.stu,pl_uslk.dzr, 
       n_opl.nopl,patient.uid,patient.fam,patient.im,patient.ot,patient.dr,
       (select nmpp from n_mpp where n_mpp.mpp=pl_uslk.vr) as nmpp,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.teh) as nteh,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.lit) as nlit,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.polir) as npolir,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.varh) as nvarh,
       (select distinct n_lpu.snlpu from n_slp,n_lpu where n_slp.slp=n_lpu.lpu and n_slp.ter=n_lpu.ter and n_slp.slp=pl_uslk.lpu) as nlpu
from pl_uslk,patient,np_otd,n_opl
Where (pl_uslk.uid=patient.uid) and (pl_uslk.otd=np_otd.otd) and (pl_uslk.opl=n_opl.opl)
  and (pl_uslk.idkv = {idkv})
order by idkv,dou"""

# sql_zakaz_naryad_select = """Select pl_uslk.idkv,pl_uslk.nkv,pl_uslk.dou,pl_uslk.stu,pl_uslk.dzr, 
#        n_opl.nopl,patient.uid,patient.fam,patient.im,patient.ot,patient.dr,
#        (select nmpp from n_mpp where n_mpp.mpp=pl_uslk.vr) as nmpp,
#        (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.teh) as nteh,
#        (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.lit) as nlit,
#        (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.polir) as npolir,
#        (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.varh) as nvarh,
#        (select nyml from np_yml where np_yml.kspr=pl_uslk.lpu and np_yml.yml=1) as nlpu
# from pl_uslk,patient,np_otd,n_opl
# Where (pl_uslk.uid=patient.uid) and (pl_uslk.otd=np_otd.otd) and (pl_uslk.opl=n_opl.opl)
#   and (np_otd.GR_OTD=2) 
#   and (pl_uslk.dou>='{dtn}' and pl_uslk.dou<='{dtk}')
# order by idkv,dou"""

# idkv, - уникальный код квитанции (не нужен)
# nkv,  - номер наряда
# dou,  - дата оформления наряда
# stu,  - полная стоимость
# dzr,  - дата закрытия
# nopl, - вид оплаты
# uid,  - номер карты пациента
# fam,  - Фамилия пац
# im,   - Имя пац
# ot,   - Отчество пац
# dr,   - дата рождения
# nmpp, - ФИО врача
# nteh, - ФИО Техника
# nlit, - ФИО Литейщика
# npolir- ФИО Полировщика 
# nvarh - ФИО Варщика
# --------------------------------------------------------------{% for idkv, nkv, dou, stu, dzr, nopl, uid, fam, im, ot, dr, nmpp, nteh, nlit, npolir, nvarh in my_list %}
sql_ad_arena_username = """select app_user from users_app where com='{}'"""
sql_ad_arena_mpp = """select mpp from users_app where com='{}'"""

# Табель учета рабочего времени
sql_TabWorkTime = """Select (select nroom_kr from room where room.id=it_rasp_grf.room),
                (select notd from np_otd where np_otd.otd=it_rasp_grf.otd),
                n_spz.nspz,n_doc.ndoc,
                it_rasp_grf.*
                from it_rasp_grf,n_doc,n_spz
                where (it_rasp_grf.doc=n_doc.doc) and (it_rasp_grf.spz=n_spz.spz)
                and it_rasp_grf.YEARWORK={EYear}
                and it_rasp_grf.MONTHWORK={EMonth}
                and it_rasp_grf.OTD={otd}"""
