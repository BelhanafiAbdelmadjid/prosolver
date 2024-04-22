'''
# extended LDIF
#
# LDAPv3
# base <ou=users,dc=jidsu-company,dc=com> with scope subtree
# filter: (uid=newuser)
# requesting: ALL
#

# newuser, users, jidsu-company.com
dn: uid=newuser,ou=users,dc=jidsu-company,dc=com
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
uid: newuser
cn: New User
sn: User
givenName: qr6
userPassword:: cXI2

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1

'''

from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from ldap3 import *
import ldap3
import ssl
 

class ldap_conn():

    def __init__(self,app):
        self.app = app
        
    def authentificate(self,username_to_auth,password_to_auth) :
        user = f'cn={self.app.config.get("LDAP_BIND_USERNAME")},{self.app.config.get("ROOT_DN")}'

        server = Server(self.app.config.get("LDAP_SERVER"), get_info=ALL)
        
        try:
            connection = Connection(server,
                        user=user,
                        password=self.app.config.get("LDAP_BIND_PASSWORD"),
                        client_strategy=SAFE_SYNC
                        )
        except  :
            raise ValueError("Authentication failed, the Active Directory server is currently unavailable.")
        if not connection.bind():
            raise ValueError("Cannot bind to LDAP!")
        else:
            username_to_auth = ""+username_to_auth
            # username_to_auth = "@dz.nxbp.corp\\"+username_to_auth
            # result = connection.rebind(user=username_to_auth,password=password_to_auth,authentication=NTLM)
            result = connection.search("ou=users,"+self.app.config.get("ROOT_DN"),f'(&(uid={username_to_auth})(userPassword={password_to_auth}))')
            return result[0]
                
        
        

# # ldap server hostname and port
# LDAP_SERVER = f"ldap://192.168.1.64:389"
# # dn
# ROOT_DN = "dc=jidsu-company,dc=com"
# # ldap user and password
# LDAP_BIND_USERNAME = 'admin'
# LDAP_BIND_PASSWORD = 'admin'
 
# # user
# user = f'cn={LDAP_BIND_USERNAME},{ROOT_DN}'

# server = Server(LDAP_SERVER, get_info=ALL)
 
# connection = Connection(server,
#                         user=user,
#                         password=LDAP_BIND_PASSWORD,
#                          client_strategy=SAFE_SYNC, auto_bind=True
#                         )

# if not connection.bind():
#     print(f" *** Cannot bind to ldap server: {connection.last_error} ")
# else:
#     print(f" *** Successful bind to ldap server")
#     result = connection.search("ou=users,"+ROOT_DN,"(&(uid=newuser)(userPassword=qr6))")
#     print(result)