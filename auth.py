import ldap

def check_credentials(username, password):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure
    # Adapt to your needs
    """
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
    # all is well
    # get all user groups and store it in session for future use
    #    cherrypy.session[username] = str(ldap_client.search_s(base_dn,
    #                    ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
    # print(str(ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf']))
    s = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
    # s = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1])
    # s = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1][''])
    d = (ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs2)[0][0])
    auth_fio = ""
    for x in s:
        x = str(x, 'utf-8')
        # print(type(x))
        chars1 = "CN="
        chars2 = ","
        # print(type(x))
        # print(x)
        # print(x.decode("utf-8", "ignore"))
        # print(x.decode())
        n = x[x.find(chars1)+3 : x.find(chars2)]
        if n == "web_hs_admin":
            auth_fio = n
            
        print(f'Состоит в группе: { n }')
        # print(n)
        # print(n.decode("utf-8", "ignore"))
        # print(x.decode("utf-8", "ignore"))
    char1 = 'CN='
    char2 = ','
    k = ""
    k = d[d.find(char1)+3 : d.find(char2)]
    print(f'ФИО: {k}')
    # print(k)
    # print(ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, attrs)[0][1]['memberOf'])
    # print(ldap_client.search_s(base_dn, ldap.SCOPE_SUBTREE, ldap_filter, )
    ldap_client.unbind()
    return "ok", k, auth_fio