import ldap
from flask import session
import app.db as db
import app.sql as sql


def check_admins_auth(username, password, user_ad):
    session.clear()
    LDAP_SERVER = 'ldap://192.168.100.2'
    # fully qualified AD user name
    LDAP_USERNAME = '%s@gsp.local' % username
    # your password
    LDAP_PASSWORD = password
    base_dn = 'DC=GSP,DC=local'
    ldap_filter = 'userPrincipalName=%s@gsp.local' % user_ad
    attrs = ['memberOf']
    attrs2 = ['displayName']
    try:
       # build a client
        ldap_client = ldap.initialize(LDAP_SERVER)
       # perform a synchronous bind
        ldap_client.set_option(ldap.OPT_REFERRALS,0)
        ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
    except ldap.INVALID_CREDENTIALS:
        ldap_client.unbind()
        return 'error', 'AD: Неверное имя пользователя или пароль'
    except ldap.SERVER_DOWN:
        return 'error', 'AD: Сервер не доступен'
    s = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
    d = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs2)[0][0]) 
    for x in s:
        x = str(x, 'utf-8')
        chars1 = "CN="
        chars2 = ","
        auth_group = x[x.find(chars1)+3 : x.find(chars2)]
        if "web_hs" in auth_group:
            # print(f'Состоит в группе: { auth_group }')
            session['auth_group'] = auth_group
        else:
            pass
            # print(f'Не состоит в группах web_hs')   
    char_start = 'CN='
    char_end = ','
    arena_fio = d[d.find(char_start)+3 : d.find(char_end)]
    # print(f'ФИО: {arena_fio}')
    arena_mpp = 000
    try:
        f = db.select(sql.sql_ad_arena_username.format(user_ad))
        arena_username = f[0][0]
        if arena_username != None:
            session['arena_user'] = arena_username
    except BaseException:
        print(BaseException)
    try:
        arena_mpp = db.select(sql.sql_ad_arena_mpp.format(user_ad))
        session['arena_mpp'] = arena_mpp[0][0]
    except BaseException:
        print(BaseException)
    arena_mpp = db.select(sql.sql_ad_arena_mpp.format(user_ad))
    session['arena_fio'] = arena_fio
    session['arena_mpp'] = arena_mpp
    ldap_client.unbind()
    return "ok", arena_fio, auth_group


def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure
    # Adapt to your needs
    """
    session.clear()
    LDAP_SERVER = 'ldap://192.168.100.2'
    # fully qualified AD user name
    LDAP_USERNAME = '%s@gsp.local' % username
    # your password
    LDAP_PASSWORD = password
    base_dn = 'DC=GSP,DC=local'
    ldap_filter = 'userPrincipalName=%s@gsp.local' % username
    attrs = ['memberOf']
    attrs2 = ['displayName']
    try:
       # build a client
        ldap_client = ldap.initialize(LDAP_SERVER)
       # perform a synchronous bind
        ldap_client.set_option(ldap.OPT_REFERRALS,0)
        ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
    except ldap.INVALID_CREDENTIALS:
        ldap_client.unbind()
        return 'error', 'AD: Неверное имя пользователя или пароль'
    except ldap.SERVER_DOWN:
        return 'error', 'AD: Сервер не доступен'
    s = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
    d = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs2)[0][0]) 
    for x in s:
        x = str(x, 'utf-8')
        chars1 = "CN="
        chars2 = ","
        auth_group = x[x.find(chars1)+3 : x.find(chars2)]
        if "web_hs" in auth_group:
            print(f'Состоит в группе: { auth_group }')
            session['auth_group'] = auth_group
        else:
            print(f'Не состоит в группах web_hs')   
    char_start = 'CN='
    char_end = ','
    arena_fio = d[d.find(char_start)+3 : d.find(char_end)]
    print(f'ФИО: {arena_fio}')
    arena_mpp = 000
    try:
        f = db.select(sql.sql_ad_arena_username.format(username))
        arena_username = f[0][0]
        if arena_username != None:
            session['arena_user'] = arena_username
    except BaseException:
        print(BaseException)
    try:
        arena_mpp = db.select(sql.sql_ad_arena_mpp.format(username))
        session['arena_mpp'] = arena_mpp[0][0]
    except BaseException:
        print(BaseException)
    arena_mpp = db.select(sql.sql_ad_arena_mpp.format(username))
    session['arena_fio'] = arena_fio
    session['arena_mpp'] = arena_mpp
    ldap_client.unbind()
    return "ok", arena_fio, auth_group
