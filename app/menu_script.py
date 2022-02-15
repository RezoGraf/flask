from flask import session


exit = """<a href="/logout" class="btn btn-danger" role="button">Выход</a>"""


def generate_menu():
    menu = ''
    if 'auth_group' in session:
      auth_group = session.get('auth_group')
    else:
      auth_group = 'web_hs_user'
    if 'arena_fio' in session:
        arena_fio = session.get('arena_fio')
    else:
      'Неавторизованный пользователь'
    if auth_group == "web_hs_admin":
        menu = f"""<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Переключатель навигации">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item">
        <a class="nav-link text-primary" href="/menu">Главная</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false" >Сотрудники</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/data_input/wtf_template3">График работы</a>
          <a class="dropdown-item text-primary" href="/htmx_test/table_view">График учета рабочего времени</a>  
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Отчеты</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/report">Отчет по отсутствующим</a>
          <a class="dropdown-item text-primary" href="/zakaz_naryad">Заказ Наряды</a>
        </div>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/report">Отчет по отсутствующим</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Вакцинация</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/vaccine">Заполнение карточек вакцинации</a>
          <a class="dropdown-item text-primary" href="/vaccine/report">Отчет о вакцинации</a>
          <a class="dropdown-item text-primary" href="/vaccine/sinc">Синхронизация справочников</a>
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Сервис</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/db_test">Тестирование БД Firebird</a>
          <a class="dropdown-item text-primary" href="/htmx_test">Тест HTMX</a>
          <a class="dropdown-item text-primary" href="/htmx_test/table_view">Таблица HTMX</a>
          <a class="dropdown-item text-primary" href="/aalksdhl28kdhalu8">Авторизация от лица пользователя</a>
          
        </div>
      </li>
    </ul>
    <form align="right" class="form-inline my-2 my-lg-0">
      <label>{arena_fio}<pre>  </pre></label>
      {exit}
    </form>
  </div>
</nav>"""

    if auth_group == 'web_hs_user':
        menu = f"""<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Переключатель навигации">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <form class="form-inline my-2 my-lg-0">
      <label>{arena_fio}<pre>  </pre></label>
      <a href="/logout" class="btn btn-secondary" role="button"> Выход</a>
    </form>
  </div>
</nav>
<body>
<h1>Helios, к сожалению у вас нет доступа. Попробуйте зайти повторно, или оставить заявку по номеру 911</h1>
</body>"""

    if auth_group == 'web_hs_kadr':
        menu = f"""<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Переключатель навигации">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item">
        <a class="nav-link text-primary" href="/menu">Главная</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false" >Сотрудники</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/data_input/wtf_template3">График работы</a> 
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Отчеты</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/report">Отчет по отсутствующим</a>
        </div>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <label>{arena_fio}<pre>  </pre></label>
      {exit}
    </form>
  </div>
</nav>"""

    if auth_group == 'web_hs_epid':
        menu = f"""<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Переключатель навигации">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item">
        <a class="nav-link text-primary" href="/menu">Главная</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false" >Сотрудники</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/data_input/wtf_template3">График работы</a> 
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Отчеты</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/report">Отчет по отсутствующим</a>
        </div>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <label>{arena_fio}<pre>  </pre></label>
      {exit}
    </form>
  </div>
</nav>"""

    if auth_group == 'web_hs_zav':
        menu = f"""<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Переключатель навигации">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
      <li class="nav-item">
        <a class="nav-link text-primary" href="/menu">Главная</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false" >Сотрудники</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/data_input/wtf_template3">График работы</a> 
        </div>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle text-primary" data-toggle="dropdown" href="#" role="button" aria-haspopup="true" aria-expanded="false">Отчеты</a>
        <div class="dropdown-menu">
          <a class="dropdown-item text-primary" href="/report">Отчет по отсутствующим</a>
        </div>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <label>{arena_fio}<pre>  </pre></label>
      {exit}
    </form>
  </div>
</nav>"""

    else:
        """<h1>Helios, к сожалению у вас нет доступа</h1>"""
    return menu