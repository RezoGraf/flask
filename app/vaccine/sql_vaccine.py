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



#------------------postgresql----------------------------------------------------

sinc_worker = """INSERT INTO public."epid_WORKER"(
	"ID_WORKER", "FAM_WORKER", "IM_WORKER", "OT_WORKER", "PODR", "OTD", "DLJ")
	VALUES ('{mpp}', '{fam}', '{im}', '{ot}', '{lpu}', '{otd}', '{dolj}')"""


sinc_vaccine = """INSERT INTO public."epid_S_VACCINE"(
	"NVACCINE", "ID_ARENA")
	VALUES ('{nvc}', '{vcid}')"""


select_workers = """SELECT "IDW", "ID_WORKER", "FAM_WORKER",
 "IM_WORKER", "OT_WORKER", "DR", "PODR", "OTD", "DLJ", "CERT"
	FROM public."epid_WORKER";"""
