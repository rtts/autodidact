from ldap3 import Server, Connection

class LDAPError(Exception):
    pass

def search_ldap(username):
    '''Searches the Tilburg University LDAP server for the given username and returns a tuple of first name, full name, ANR and email address. Permission has been granted by TiU's legal department for retrieving this data. Raises LDAPError on any kind of error.'''

    result = ()
    baseDN = "o=Universiteit van Tilburg,c=NL"
    searchFilter = '(uid={})'.format(username)
    attributes = ['givenName', 'cn', 'employeeNumber', 'mail']

    try:
        server = Server('ldaps.uvt.nl', use_ssl=True)
        conn = Connection(server, auto_bind=True)
        conn.search(baseDN, searchFilter, attributes=attributes)
        for a in attributes:
            result += (conn.response[0]['attributes'][a][0], )
    except Exception:
        raise LDAPError('Error in LDAP query')

    return result
