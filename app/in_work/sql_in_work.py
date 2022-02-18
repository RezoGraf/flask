sql_all_today = """Select it_rasp.doc,np_otd.notd,n_mpp.nmpp,n_mpp.tel, 
 (select ndlj as nspz from n_dlj where n_doc.dolj=n_dlj.dlj),
 (select nroom_kr from room where room.id=it_rasp.room),
 (select SNLPU from n_lpu where ter=5 and N_LPU.LPU=N_DOC.LPU) as SNLPU,
 CASE 
  WHEN (EXTRACT(WEEK from dateoff)=EXTRACT(WEEK from Cast('{today}' as Date))) and (it_rasp.dateoff>=Cast('{today}' as Date)) then NULL 
  ELSE it_rasp.even_day END as even_day,
 CASE 
  WHEN (EXTRACT(WEEK from dateoff)=EXTRACT(WEEK from Cast('{today}' as Date))) and (it_rasp.dateoff>=Cast('{today}' as Date)) then NULL 
  ELSE it_rasp.noeven_day END as noeven_day 
From it_rasp,np_otd,n_doc,n_mpp 
Where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc) 
  and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) 
order by SNLPU,NOTD,NMPP"""


sql_all_otd = """Select distinct np_otd.notd
From it_rasp,np_otd,n_doc,n_mpp 
Where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc) 
  and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and np_otd.notd is not Null"""

sql_all_podr = """Select distinct
 (select SNLPU from n_lpu where ter=5 and N_LPU.LPU=N_DOC.LPU) as SNLPU
From it_rasp,np_otd,n_doc,n_mpp 
Where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc) 
  and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1)"""


# sql_all_today = """Select it_rasp.doc,np_otd.notd,n_mpp.nmpp,n_mpp.tel, 
#  (select ndlj as nspz from n_dlj where n_doc.dolj=n_dlj.dlj),
#  (select nroom_kr from room where room.id=it_rasp.room),
#  (select SNLPU from n_lpu where ter=5 and N_LPU.LPU=N_DOC.LPU) as SNLPU,
#  CASE 
#   WHEN (EXTRACT(WEEK from dateoff)=EXTRACT(WEEK from Cast('{today}' as Date))) and (it_rasp.dateoff>=Cast('{today}' as Date)) then NULL 
#   ELSE it_rasp.even_day END as even_day,
#  CASE 
#   WHEN (EXTRACT(WEEK from dateoff)=EXTRACT(WEEK from Cast('{today}' as Date))) and (it_rasp.dateoff>=Cast('{today}' as Date)) then NULL 
#   ELSE it_rasp.noeven_day END as noeven_day 
# From it_rasp,np_otd,n_doc,n_mpp 
# Where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc) 
#   and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) 
# order by SNLPU,NOTD,NMPP"""