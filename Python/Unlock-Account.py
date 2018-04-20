import os
import sys
import logging
from pathlib import Path
from ldap3 import Server, Connection, ALL, MODIFY_REPLACE
import getpass
from datetime import datetime ,date ,time ,timedelta ,timezone

#SCRIPT OPTIONS
ldap_username = 'ryan@cs.odu.edu'
search_ou = 'DC=cs,DC=odu,DC=edu'

ldap_filter = '(&(objectCategory=person)(objectClass=user)(sAMAccountName=%s))' % str(sys.argv[1])

#Attributes that you want displayed
attributes = ["distinguishedName"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Unlock-Account.py')

#Obtain LDAP Password
ldap_pass = getpass.getpass("LDAP Password:")

#LDAP Server Connect
server = Server('ad.cs.odu.edu', get_info=ALL)
conn = Connection(server, ldap_username, ldap_pass, auto_bind=True)
conn.search(search_ou,ldap_filter,attributes=attributes)

#Loop through the search results. Ideally there should be only one, since sAMAccountNames are unique to users. Nonetheless, Loop through all of them just incase the script usage changes.
for user in conn.entries:
    dn = user.distinguishedName.value
    conn.modify(dn, {'lockoutTime': [(MODIFY_REPLACE, ['0'])]})
    print(conn.result)


conn.unbind()