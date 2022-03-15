"""Запрос на выбор всех людей из БД Firebird (Арена)"""
select_all_mpp = """
    select distinct mpp,
        (select fam from n_mpp where n_mpp.mpp=n_doc.mpp) as fam,
        (select im from n_mpp where n_mpp.mpp=n_doc.mpp) as im,
        (select ot from n_mpp where n_mpp.mpp=n_doc.mpp) as ot,
    lpu,otd,spz,dolj,sdl 
    from n_doc 
    where pv=1 and mol=1 
    order by mpp
    """

select_one_mpp = """
    select distinct mpp,
        (select fam from n_mpp where n_mpp.mpp=n_doc.mpp) as fam,
        (select im from n_mpp where n_mpp.mpp=n_doc.mpp) as im,
        (select ot from n_mpp where n_mpp.mpp=n_doc.mpp) as ot,
    lpu,otd,spz,dolj,sdl 
    from n_doc 
    where pv=1 and mol=1 and mpp={mpp}
    """


select_vaccine = """select VVC, NVVC from n_vvc where VVC>0"""


select_podr = """select lpu,snlpu from n_lpu where ter=5 and tmo=73"""


select_dolj = """select DLJ, NDLJ from N_DLJ where DLJ>0"""


select_spz = """select spz, nspz from n_spz where spz>0"""


select_sdl = """select sdl,nsdl from n_mpp_sdl where sdl>0"""


select_otd = """select OTD,NOTD,LPU,NOTD_KR from np_otd where otd>0"""


#------------------postgresql----------------------------------------------------

sinc_worker = """INSERT INTO public."epid_WORKER"(
	"ID_WORKER", "FAM_WORKER", "IM_WORKER", "OT_WORKER", "PODR", "OTD", "DLJ", "SPZ", "SDL")
	VALUES ('{mpp}', '{fam}', '{im}', '{ot}', '{lpu}', '{otd}', '{dolj}', '{spz}', '{sdl}')"""


sinc_vaccine = """INSERT INTO public."epid_S_VACCINE"(
	"NVACCINE", "ID_ARENA")
	VALUES ('{nvc}', '{vcid}')"""


sinc_podr = """INSERT INTO public."epid_S_PODR"(
    "ID", "NPODR")
    VALUES ('{id}', '{npodr}')"""


sinc_dolj = """INSERT INTO public."epic_S_DOLJ"(
	"ID", "NDLJ")
	VALUES ('{id}', '{ndlj}')"""


sinc_spz = """INSERT INTO public."epic_S_SPZ"(
	"ID", "NSPZ")
	VALUES ('{id}', '{nspz}');"""


sinc_sdl = """INSERT INTO public."epid_S_SDL"(
	"ID", "NSDL")
	VALUES ('{id}', '{nsdl}');"""

sinc_otd = """INSERT INTO public."epic_S_OTD"(
	"ID", "NOTD", "NOTD_KR", "LPU")
	VALUES ('{id}', '{notd}', '{notd_kr}', '{lpu}');"""


select_workers = """SELECT "IDW", "FAM_WORKER",
 "IM_WORKER", "OT_WORKER", "DR", "PODR", "OTD", "DLJ", "SPZ", "SDL", "CERT"
	FROM public."epid_WORKER";"""

select_workers_for_start = """SELECT public."epid_WORKER"."IDW", public."epid_WORKER"."FAM_WORKER",
 public."epid_WORKER"."IM_WORKER", public."epid_WORKER"."OT_WORKER", public."epid_WORKER"."DR", 
 public."epid_S_PODR"."NPODR", public."epid_S_OTD"."NOTD", public."epid_S_DOLJ"."NDLJ", 
 public."epid_S_SPZ"."NSPZ", public."epid_S_SDL"."NSDL", public."epid_WORKER"."CERT"
 
  FROM public."epid_WORKER" 
  	left join public."epid_S_PODR" on public."epid_WORKER"."PODR"=public."epid_S_PODR"."ID"
	left join public."epid_S_OTD" on public."epid_WORKER"."OTD"=public."epid_S_OTD"."ID"
	left join public."epid_S_DOLJ" on public."epid_WORKER"."DLJ"=public."epid_S_DOLJ"."ID"
	left join public."epid_S_SPZ" on public."epid_WORKER"."SPZ"=public."epid_S_SPZ"."ID"
	left join public."epid_S_SDL" on public."epid_WORKER"."SDL"=public."epid_S_SDL"."ID" """


select_workers_fio = """ SELECT public."epid_WORKER"."IDW", concat(public."epid_WORKER"."FAM_WORKER", ' ',
 public."epid_WORKER"."IM_WORKER", ' ', public."epid_WORKER"."OT_WORKER") as "FIO", public."epid_WORKER"."DR", 
 public."epid_S_PODR"."NPODR", public."epid_S_OTD"."NOTD", public."epid_S_DOLJ"."NDLJ", 
 public."epid_S_SPZ"."NSPZ", public."epid_S_SDL"."NSDL", public."epid_WORKER"."CERT"
 
  FROM public."epid_WORKER" 
  	left join public."epid_S_PODR" on public."epid_WORKER"."PODR"=public."epid_S_PODR"."ID"
	left join public."epid_S_OTD" on public."epid_WORKER"."OTD"=public."epid_S_OTD"."ID"
	left join public."epid_S_DOLJ" on public."epid_WORKER"."DLJ"=public."epid_S_DOLJ"."ID"
	left join public."epid_S_SPZ" on public."epid_WORKER"."SPZ"=public."epid_S_SPZ"."ID"
	left join public."epid_S_SDL" on public."epid_WORKER"."SDL"=public."epid_S_SDL"."ID" """


select_workers_main = """SELECT public."epid_WORKER"."IDW", concat(public."epid_WORKER"."FAM_WORKER", ' ',
 public."epid_WORKER"."IM_WORKER", ' ', public."epid_WORKER"."OT_WORKER") as "FIO", 
 public."epid_S_PODR"."NPODR", public."epid_S_OTD"."NOTD", public."epid_S_DOLJ"."NDLJ", 
 public."epid_WORKER"."CERT"
 
  FROM public."epid_WORKER" 
  	left join public."epid_S_PODR" on public."epid_WORKER"."PODR"=public."epid_S_PODR"."ID"
	left join public."epid_S_OTD" on public."epid_WORKER"."OTD"=public."epid_S_OTD"."ID"
	left join public."epid_S_DOLJ" on public."epid_WORKER"."DLJ"=public."epid_S_DOLJ"."ID";"""


select_workers_search = """SELECT public."epid_WORKER"."IDW", concat(public."epid_WORKER"."FAM_WORKER", ' ',
 public."epid_WORKER"."IM_WORKER", ' ', public."epid_WORKER"."OT_WORKER") as "FIO", 
 public."epid_S_PODR"."NPODR", public."epid_S_OTD"."NOTD", public."epid_S_DOLJ"."NDLJ", 
 public."epid_WORKER"."CERT"
 
  FROM public."epid_WORKER" 
  	left join public."epid_S_PODR" on public."epid_WORKER"."PODR"=public."epid_S_PODR"."ID"
	left join public."epid_S_OTD" on public."epid_WORKER"."OTD"=public."epid_S_OTD"."ID"
	left join public."epid_S_DOLJ" on public."epid_WORKER"."DLJ"=public."epid_S_DOLJ"."ID"
	WHERE public."epid_WORKER"."FAM_WORKER" like '%{search}%';"""

select_workers_fam = """SELECT public."epid_WORKER"."FAM_WORKER"
 
  FROM public."epid_WORKER" 
  	left join public."epid_S_PODR" on public."epid_WORKER"."PODR"=public."epid_S_PODR"."ID"
	left join public."epid_S_OTD" on public."epid_WORKER"."OTD"=public."epid_S_OTD"."ID"
	left join public."epid_S_DOLJ" on public."epid_WORKER"."DLJ"=public."epid_S_DOLJ"."ID";"""


select_worker_by_id = """
SELECT public."epid_WORKER"."IDW", public."epid_WORKER"."FAM_WORKER",
 public."epid_WORKER"."IM_WORKER", public."epid_WORKER"."OT_WORKER", public."epid_WORKER"."DR", 
 public."epid_S_PODR"."NPODR", public."epid_S_OTD"."NOTD", public."epid_S_DOLJ"."NDLJ", 
 public."epid_S_SPZ"."NSPZ", public."epid_S_SDL"."NSDL", public."epid_WORKER"."CERT"
 
  FROM public."epid_WORKER" 
    left join public."epid_S_PODR" on public."epid_WORKER"."PODR"=public."epid_S_PODR"."ID"
  left join public."epid_S_OTD" on public."epid_WORKER"."OTD"=public."epid_S_OTD"."ID"
  left join public."epid_S_DOLJ" on public."epid_WORKER"."DLJ"=public."epid_S_DOLJ"."ID"
  left join public."epid_S_SPZ" on public."epid_WORKER"."SPZ"=public."epid_S_SPZ"."ID"
  left join public."epid_S_SDL" on public."epid_WORKER"."SDL"=public."epid_S_SDL"."ID"
  
  WHERE public."epid_WORKER"."IDW"='{idw}';"""

sel_all_vaccine = """
SELECT "VACCINE", "NVACCINE"
	FROM public."epid_S_VACCINE";"""