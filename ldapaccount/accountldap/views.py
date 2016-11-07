import sys
sys.path.append('/home/annmoon/py3-ldap/accountmanager/accountLib/ldap')
sys.path.append('/home/annmoon/py3-ldap/accountmanager/accountLib/mail')

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from ldapmain import simple_bind, ldap_search, user_add, get_bindinfo, increment_uidNumber, get_email, get_password, password_reset
from ldaptoken import default_token_generator
from .forms import useraddForm, userPWForm, SetPasswordForm
from sendmail import send_mail_boto3

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Create your views here.
def index(request):
	return render(request, 'accountldap/index.html', {'data' : 'LDAP TOOL'})


def userList(request):

	bind_dn = get_bindinfo('ldap-user1')

	users = ldap_search('ldap.annmoon.com', 'cn={username},ou=People,dc=annmoon,dc=com'.format(**bind_dn), '{password}'.format(**bind_dn))
	return render(request, 'accountldap/list.html', {'data' : users})


def userAdd(request):
	if request.method == 'POST':
		form = useraddForm(request.POST)
		if form.is_valid():

			uid = form.cleaned_data['uid']
			userPassword = form.cleaned_data['userPassword']
			confirm_userPassword = form.cleaned_data['confirm_userPassword']

			mail = form.cleaned_data['mail']
			sn = form.cleaned_data['sn']
			givenName = form.cleaned_data['givenName']
			host = form.cleaned_data['host']
			gidNumber = form.cleaned_data['gidNumber']

			if "," in host:
				host_list = host.split(",")
				host_tuple = tuple(host_list)

			bind_dn = get_bindinfo('ldap-Manager')

			kwargs={
				'uid': uid, 
				'userPassword': userPassword, 
				'mail': mail, 
				'sn': sn, 
				'givenName': givenName, 
				'gidNumber': gidNumber, 
				# for ldap bind
				'servername': 'ldap.annmoon.com', 
				'user_dn': 'cn={username},dc=annmoon,dc=com'.format(**bind_dn), 
				'user_password':'{password}'.format(**bind_dn)
			}
			add_new_user = user_add(*host_tuple, **kwargs)

			if add_new_user:
				if add_new_user == "001":
					msg = "this user is already exist"
				elif add_new_user == "002":
					msg = "you don't input valid user id. please input user id again"
				elif add_new_user == "003":
					msg = "can't get new uid number"
				elif add_new_user == "004":
					msg = "can't bind ldap"
				else:
					msg = ""


				if msg == "":
					## increment uidnumber
					new_uid_number = increment_uidNumber('ldap.annmoon.com', 'cn={username},dc=annmoon,dc=com'.format(**bind_dn), '{password}'.format(**bind_dn))
					if new_uid_number:

						## send password reset mail
						return HttpResponseRedirect('/accountldap/users/')

						#return userAddPWsend(request, uid, mail)
					else:
						return render(request, 'accountldap/msg.html', {'user_data': 'failed increment uid number but, new user added.'})
				else:
					return render(request, 'accountldap/msg.html', {'user_data': msg})

			else:
				return render(request, 'accountldap/msg.html', {'user_data': 'failed add user'})

	else:
		form = useraddForm()

	return render(request, 'accountldap/add.html', {'form': form})

## send password reset mail
def userPWsend(request):
	if request.method == 'POST':
		form = userPWForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data["user_id"]
		
			if data:

				bind_dn = get_bindinfo('ldap-user1')

				## get email
				email_address = get_email('ldap.annmoon.com', 'cn={username},ou=People,dc=annmoon,dc=com'.format(**bind_dn), '{password}'.format(**bind_dn), data)

				if email_address:
					## send email 
					c = {
						'email': email_address,
						'domain': 'http://annmoon.com',
						'site_name': 'LDAP',
						'uid': urlsafe_base64_encode(force_bytes(data)),
						'user': data,
						'token': default_token_generator.make_token(data),
					}

					email_to_list = []
					email_to_list.append(email_address)

					email_template_name='accountldap/pw_reset_email.html'
					email = render_to_string(email_template_name, c)

					send_mail_boto3(email_to_list, email)

					msg = 'Email has been sent to ' + email_address + '. Please check its inbox to continue reseting password.'

					return render(request, 'accountldap/msg.html', {'user_data': msg})
				else:
					return render(request, 'accountldap/msg.html', {'user_data': 'failed to get email'})
	else:
		form = userPWForm()

	return render(request, 'accountldap/pw.html', {'form': form})

## send password reset mail from adding user.
def userAddPWsend(request, uid, to_email):
	#if 'uid' in request.GET and 'to_email' in request.GET:
	if uid is not None and uid != '' and to_email is not None and to_email != '':

		#if uid is not None and uid != '' and to_email is not None and to_email != '':
		email_to_list = []
		email_to_list.append(to_email)

		c = {
			'email': to_email,
			'domain': 'http://annmoon.com',
			'site_name': 'LDAP',
			'uid': urlsafe_base64_encode(force_bytes(uid)),
			'user': uid,
			'token': default_token_generator.make_token(uid),
		}

		email_template_name='accountldap/pw_reset_email.html'
		email = render_to_string(email_template_name, c)

		send_mail_boto3(email_to_list, email)
		msg = 'Email has been sent to ' + to_email + '. Please check its inbox to continue reseting password.'

		return render(request, 'accountldap/msg.html', {'user_data': msg})

	else:
		return render(request, 'accountldap/msg.html', {'user_data': 'failed to get email, no uid, no email'})


## reset user password
def userPWreset(request, uidb64=None, token=None):
	if request.method == 'POST':
		form = SetPasswordForm(request.POST)
		uidb64 = request.POST.get('uidb64', None)
		token = request.POST.get('token', None)
		
		assert uidb64 is not None and token is not None
		
		try:
			uid = urlsafe_base64_decode(uidb64)
		except (TypeError, ValueError, OverflowError):
			uid = None
		
		if uid is not None and default_token_generator.check_token(force_text(uid), token):
			if form.is_valid():
				new_password= form.cleaned_data['new_password2']

				## ldap bind
				
				bind_dn = get_bindinfo('ldap-user1')
				result = password_reset('ldap.annmoon.com', 'cn={username},dc=annmoon,dc=com'.format(**bind_dn), '{password}'.format(**bind_dn), force_text(uid), new_password)
				
				if result:
					return render(request, 'accountldap/msg.html', {'user_data': 'Password has been changed.'})
				else:
					return render(request, 'accountldap/msg.html', {'user_data': 'failed password change.'})

	else:
		## url token check
		if default_token_generator.check_token(force_text(urlsafe_base64_decode(uidb64)), token):
			form = SetPasswordForm()
			assert uidb64 is not None and token is not None
		else:
			return render(request, 'accountldap/msg.html', {'user_data': 'This URL is not valid anymore'})


	return render(request, 'accountldap/pw_reset.html', {'form': form, 'uidb64': uidb64, 'token': token})




