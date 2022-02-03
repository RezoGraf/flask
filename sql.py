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

# Выбор списка доступных отделений
sql_allOtd = "select otd, notd from np_otd where otd>=0 {select_otd} order by ps"
# Выбор текущего отделения
sql_currentOtd = "select otd, notd, lpu from np_otd where otd='{otd}'"

# Выборка первого попавшегося отделения
sql_randomOtd = """select first 1 otd from np_otd where otd>0 {select_otd} order by otd"""
sql_randomOtd1 = "select otd, notd, lpu from np_otd where otd>0 {select_otd}"
# Выборка доступных отделений
sql_accessOtd = """select txt from users_set_app where app_user='{arena_user}' and mdl=88 and set_code=20000 """
# Выборка доступных должностей
sql_accessSdl = """select txt from users_set_app where app_user='{arena_user}' and mdl=88 and set_code=20001 """

# Выборка всех ФИО врачей по коду отделения
sql_allDoc = """select n_doc.doc, n_doc.ndoc||' ('||n_dlj.ndlj||')' as ndoc from n_doc, n_dlj 
                where (n_doc.dolj=n_dlj.dlj) and (n_doc.pv=1) and (n_doc.pr_dlj=1) and (mol=1) {current_otd}
                {select_sdl} 
                order by ndoc """
# Выборка первого попавшегося врача
sql_randomDoc = """select first 1 doc from n_doc where pv=1 and doc>0 {select_otd} {select_sdl} order by ndoc"""
# Выборка ФИО по коду
sql_fio_sotrudnika = """select distinct n_mpp.nmpp from n_doc, n_mpp where (n_doc.mpp=n_mpp.mpp) and n_doc.doc={doc} """

# Причина отсутствия на рабочем месте
sql_rsp_rsn = """select rsn, nrsn from rsp_rsn order by rsn"""

# Номера кабинетов
sql_room = """select id, nroom_kr from room where lpu in (select distinct lpu from n_doc where doc={doc}) order by id"""

# Выборка всех специальностей сотрудников
sql_allSpz = """select spz, nspz from n_spz where pd=1 order by nspz"""

# Информация о режиме работы сотрудника
sql_it_rasp = """Select IT_RASP.ROOM,
                        ROOM.NROOM_KR,
                        IT_RASP.ID_INTERVAL1,
                        (select interval_time from it_rasp_time where it_rasp_time.id=it_rasp.ID_INTERVAL1) as NOEVEN_DAY,
                        IT_RASP.ID_INTERVAL2,
                        (select interval_time from it_rasp_time where it_rasp_time.id=it_rasp.ID_INTERVAL2) as EVEN_DAY,
                        IT_RASP.NTV,
                        IT_RASP.NLIST,
                        IT_RASP.SPZ,
                        N_SPZ.NSPZ 
                 from IT_RASP, ROOM, N_SPZ 
                 where (it_rasp.room=room.id) and (it_rasp.spz=n_spz.spz) and doc='{doc}'"""

# Информация об отсутствии на работе
sql_noWork = """Select iblc, CAST (dtn AS date), CAST (dtk AS date), rsn, (select nrsn from rsp_rsn where rsp_rsn.rsn=rsp_blc.rsn) as nrsn_ 
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
sql_interval_time = """select id, case when interval_time is null THEN 'нет приема' else interval_time END from it_rasp_time order by id"""

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
       (select mpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.teh) as teh,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.lit) as nlit, 
       (select mpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.lit) as lit,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.polir) as npolir, 
       (select mpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.polir) as polir,
       (select nmpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.varh) as nvarh, 
       (select mpp from pl_uslt,n_mpp where pl_uslt.idkv=pl_uslk.idkv and n_mpp.mpp=pl_uslt.varh) as varh,
       (select distinct n_lpu.snlpu from n_slp,n_lpu where n_slp.slp=n_lpu.lpu and n_slp.ter=n_lpu.ter and n_slp.slp=pl_uslk.lpu) as nlpu
from pl_uslk,patient,np_otd,n_opl
Where (pl_uslk.uid=patient.uid) and (pl_uslk.otd=np_otd.otd) and (pl_uslk.opl=n_opl.opl)
  and (pl_uslk.idkv = {idkv})
order by idkv,dou"""
# Услуги по наряду--------------------------------------------------------------------------------------------------------
sql_zn_naryad_select_usl = """select pl_uslp.usl,pl_uslp.kusl,n_usl.nusl,pl_uslp.price,pl_uslp.kol,pl_uslp.stu
                               from pl_uslp, n_usl
                               where (pl_uslp.usl=n_usl.usl)
                               and (pl_uslp.idkv={idkv})"""
# Все исполнители для списка модального окна-------------------------------------------------------------------------------
sql_zn_naryad_select_teh = """Select distinct mpp, ndoc
                              from n_doc
                              where pv=1 and ((dolj=124 or dolj=130 ) or doc=0)
                              order by ndoc"""
sql_zn_naryad_select_lit = """Select distinct mpp, ndoc
                              from n_doc
                              where pv=1 and (dolj=163 or doc=0)
                              order by ndoc"""
sql_zn_naryad_select_pol = """Select distinct mpp, ndoc
                              from n_doc
                              where pv=1 and (dolj=162 or doc=0)
                              order by ndoc"""
sql_zn_naryad_select_var = """Select distinct mpp, ndoc
                              from n_doc
                              where pv=1 and (dolj=164 or doc=0)
                              order by ndoc"""

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
sql_TabelWorkTime = """Select it_rasp_grf.id_grf, it_rasp_grf.yearwork, it_rasp_grf.monthwork, 
                (select nroom_kr from room where room.id=it_rasp_grf.room) as nroom,
                (select notd from np_otd where np_otd.otd=it_rasp_grf.otd) as notd,
                n_spz.nspz, n_doc.ndoc,  
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day01) as day01, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day02) as day02, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day03) as day03, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day04) as day04, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day05) as day05, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day06) as day06,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day07) as day07, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day08) as day08, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day09) as day09, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day10) as day10,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day11) as day11,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day12) as day12, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day13) as day13, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day14) as day14, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day15) as day15, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day16) as day16, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day17) as day17, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day18) as day18,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day19) as day19, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day20) as day20, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day21) as day21, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day22) as day22, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day23) as day23, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day24) as day24,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day25) as day25, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day26) as day26, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day27) as day27, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day28) as day28, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day30) as day30,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day31) as day31
                from it_rasp_grf,n_doc,n_spz
                where (it_rasp_grf.doc=n_doc.doc) and (it_rasp_grf.spz=n_spz.spz)
                and it_rasp_grf.YEARWORK={EYear}
                and it_rasp_grf.MONTHWORK={EMonth}
                and it_rasp_grf.OTD={otd}"""


sql_htmx_text_tablevew = """Select it_rasp_grf.id_grf, (select nroom_kr from room where room.id=it_rasp_grf.room) as nroom,
                (select notd from np_otd where np_otd.otd=it_rasp_grf.otd) as notd,
                n_spz.nspz,n_doc.ndoc, it_rasp_grf.id_grf, it_rasp_grf.yearwork, it_rasp_grf.monthwork, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day01) as day01, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day02) as day02, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day03) as day03, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day04) as day04, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day05) as day05, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day06) as day06,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day07) as day07, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day08) as day08, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day09) as day09, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day10) as day10,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day11) as day11,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day12) as day12, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day13) as day13, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day14) as day14, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day15) as day15, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day16) as day16, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day17) as day17, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day18) as day18,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day19) as day19, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day20) as day20, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day21) as day21, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day22) as day22, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day23) as day23, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day24) as day24,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day25) as day25, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day26) as day26, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day27) as day27, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day28) as day28, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day29) as day29, 
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day30) as day30,
                (select it_rasp_time.interval_time from it_rasp_time where it_rasp_time.id=it_rasp_grf.day31) as day31
                from it_rasp_grf,n_doc,n_spz
                where (it_rasp_grf.doc=n_doc.doc) and (it_rasp_grf.spz=n_spz.spz)
                and it_rasp_grf.YEARWORK=2021
                and it_rasp_grf.MONTHWORK=12
                and it_rasp_grf.OTD=12"""
                
                
sql_interval_time_list = """select id, interval_time from it_rasp_time"""

sql_interval_time_current = """select interval_time from it_rasp_time where id={id}"""


#запрос для выборки отсутствующих для report
sql_select_otsut = """Select N_DOC.NDOC, (SELECT SNLPU FROM N_LPU WHERE N_DOC.LPU=N_LPU.LPU and N_LPU.TER=5),
    (SELECT NRSN FROM RSP_RSN WHERE RSP_RSN.RSN=RSP_BLC.RSN),RSP_BLC.DTN ,RSP_BLC.DTK
from RSP_BLC,N_DOC
where (RSP_BLC.DOC=N_DOC.DOC) and ((RSP_BLC.DTK>='{date_start}'
    and RSP_BLC.DTK<='{date_finish}') or (RSP_BLC.DTN>='{date_start}' and RSP_BLC.DTN<='{date_finish}'))"""
                