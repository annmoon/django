# -*- coding: utf-8 -*-

# import class and constants
from ldap3 import Server, Connection, ALL, SUBTREE, MODIFY_INCREMENT, MODIFY_REPLACE, MODIFY_ADD
from passlib.hash import ldap_salted_sha1 as sha
from django import forms
import hashlib, os
import netrc

def get_bindinfo(hostname):
	secrets = netrc.netrc()
	username, account, password = secrets.authenticators( hostname )

	dict = {'username': username, 'password': password}
	return dict

## get password for one time link
def get_password(userid):
	bind = get_bindinfo('ldap-Manager')
	s = Server('ldap.annmoon.com', get_info=ALL)
	c = Connection(s, user='cn={username},dc=annmoon,dc=com'.format(**bind), password='{password}'.format(**bind))

	if not c.bind():
		return c.result
	else:
		c.search(search_base = 'cn={},ou=People,dc=annnmoon,dc=com'.format(userid),
			search_filter = '(objectClass=inetOrgPerson)',
			search_scope = SUBTREE,
			attributes = ['userPassword'],
			paged_size = 5)

		#print(c)

		if c:
			pw = c.entries[0]['userPassword'].value
			return pw
		else:
			return c.result

## simple bind
def simple_bind(servername, user_dn, user_password) :
	s = Server(servername, get_info=ALL)
	c = Connection(s, user=user_dn, password=user_password)

	if not c.bind():
		return c.result
	else:
		return c.bind()


## ldap search
def ldap_search(servername, user_dn, user_password):
	s = Server(servername, get_info=ALL)
	c = Connection(s, user=user_dn, password=user_password)

	if not c.bind():
		return c.result
	else:

		entry_list = c.extend.standard.paged_search(search_base = 'ou=People,dc=annmoon,dc=com',
			search_filter = '(objectClass=inetOrgPerson)',
			search_scope = SUBTREE,
			attributes = ['cn', 'mail', 'host', 'gidNumber'],
			paged_size = 5,
			generator=False)

		return entry_list

## get uidNumber
def get_uidNumber(servername, user_dn, user_password):
	s = Server(servername, get_info=ALL)
	c = Connection(s, user=user_dn, password=user_password)

	if not c.bind():
		return c.result
	else:

		c.search(search_base = 'cn=uidNext,dc=annmoon,dc=com',
         search_filter = '(objectClass=uidNext)',
         search_scope = SUBTREE,
         attributes = ['uidNumber'],
         paged_size = 5)

		uid = c.entries[0]['uidNumber'].value

		return uid

# get email
def get_email(servername, user_dn, user_password, userid):
	s = Server(servername, get_info=ALL)
	c = Connection(s, user=user_dn, password=user_password)

	if not c.bind():
		return c.result
	else:
		c.search(search_base = 'cn={},ou=People,dc=annmoon,dc=com'.format(userid),
			search_filter = '(objectClass=inetOrgPerson)',
			search_scope = SUBTREE,
			attributes = ['mail'],
			paged_size = 5)

		email = c.entries[0]['mail'].value

		return email

## increment uidNumber
def increment_uidNumber(servername, user_dn, user_password):
	s = Server(servername, get_info=ALL)
	c = Connection(s, user=user_dn, password=user_password)

	if not c.bind():
		return c.result
	else:
		inc = c.modify('cn=uidNext,dc=annmoon ,dc=com', {'uidNumber': [(MODIFY_INCREMENT, [1])]})

		return inc


## password reset
def password_reset(servername, user_dn, user_password, user, new_pw):
	s = Server(servername, get_info=ALL)
	c = Connection(s, user=user_dn, password=user_password)

	if not c.bind():
		return c.result
	else:
		pw_reset = c.modify('cn={},ou=People,dc=annmoon,dc=com'.format(user), {'userPassword': [(MODIFY_REPLACE, [sha.encrypt('{}'.format(new_pw))])]})

		return pw_reset


## user add
def user_add(*args, **kwargs):
	if kwargs['servername'] and kwargs['user_dn'] and kwargs['user_password']:
		uid_Number = get_uidNumber(str(kwargs['servername']), str(kwargs['user_dn']), str(kwargs['user_password']))

		if isinstance( uid_Number, int ):
			s = Server(str(kwargs['servername']), get_info=ALL)
			c = Connection(s, user=str(kwargs['user_dn']), password=str(kwargs['user_password']))

			if not c.bind():
				return c.result
			else:

				## uid check
				if isinstance(kwargs['uid'], str):

					ex_uid = c.compare('cn={uid},ou=People,dc=annmoon,dc=com'.format(**kwargs), 'uid', '{uid}'.format(**kwargs))

					if not ex_uid:

						add_dict = {'gidNumber': '{gidNumber}'.format(**kwargs),
							'homeDirectory' : '/home/{uid}'.format(**kwargs),
							'sn' : '{sn}'.format(**kwargs),
							'uid' : '{uid}'.format(**kwargs),
							'uidNumber' : uid_Number,
							'gecos' : '{uid}'.format(**kwargs),
							'givenName' : '{givenName}'.format(**kwargs),
							'loginShell' : '/bin/bash',
							'mail' : '{mail}'.format(**kwargs),
							'userPassword' : sha.encrypt('{userPassword}'.format(**kwargs)) 
						}

						new_user = c.add('cn={uid},ou=People,dc=annmoon,dc=com'.format(**kwargs), 
							['inetOrgPerson', 'organizationalPerson', 'person', 'top', 'posixAccount', 'shadowAccount', 'extensibleObject'],
							add_dict
						)

						if new_user:
							if args:
								for i in args:
									if i:
										c.modify('cn={uid},ou=People,dc=annmoon,dc=com'.format(**kwargs), {'host': [(MODIFY_ADD, [i])]})
						
						return new_user

					else:
						## exist uid
						return "001"
				else:
					## no input uid
					return "002"
		else:
			## no uid number
			return "003"
	else:
		## no bind info
		return "004"
