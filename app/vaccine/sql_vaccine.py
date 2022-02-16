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
