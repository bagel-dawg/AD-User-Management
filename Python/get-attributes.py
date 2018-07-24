#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from ldap3 import Server, Connection, ALL
import getpass
import argparse

#SCRIPT OPTIONS
ldap_username = 'ryan@cs.odu.edu'
search_ou = 'DC=cs,DC=odu,DC=edu'
ldap_server = 'ad.cs.odu.edu'

parser = argparse.ArgumentParser()
arg_group = parser.add_mutually_exclusive_group(required=True)
arg_group.add_argument('-u','--uid', help='User\'s uidNumber to search for.')
arg_group.add_argument('-s', '--sAMAccountName', help='User\'s sAMAccountName to search for.')
arg_group.add_argument('-i', '--uin', help='User\'s UIN to search for.')
args = parser.parse_args()

if args.uid:
    ldap_filter = '(&(objectCategory=person)(objectClass=user)(uidNumber=%s))' % str(args.uid)

if args.sAMAccountName:
    ldap_filter = '(&(objectCategory=person)(objectClass=user)(sAMAccountName=%s))' % str(args.sAMAccountName)

if args.uin:
    ldap_filter = '(&(objectCategory=person)(objectClass=user)(employeeNumber=%s))' % str(args.uin)

#Attributes that you want displayed
attributes = ["DisplayName", "EmployeeNumber", "HomeDirectory"  , "midas",  "loginshell" , "gidNumber", "uidNumber", "PwdLastSet", "ProfilePath", "sAMAccountName", "BadPasswordTime", "extensionattribute1", "WhenCreated","lastLogon", "lastLogonTimestamp","lockoutTime"]

#Obtain LDAP Password
ldap_pass = getpass.getpass("LDAP Password:")

#LDAP Server Connect
server = Server(ldap_server, get_info=ALL)
conn = Connection(server, ldap_username, ldap_pass, auto_bind=True)
conn.search(search_ou,ldap_filter,attributes=attributes)

#Loop through the search results and display. The loop is really nice for finding duplicate IDs.
for user in conn.entries:
    print(user)

conn.unbind()
