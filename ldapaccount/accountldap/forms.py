# forms.py

from django import forms

class useraddForm(forms.Form):
	uid = forms.CharField(label='user id', max_length=20)
	userPassword = forms.CharField(label='password', max_length=30, widget=forms.PasswordInput)
	confirm_userPassword = forms.CharField(label='confirm new password', max_length=30, widget=forms.PasswordInput)
	mail = forms.EmailField()
	sn = forms.CharField(label='surname', max_length=20)
	givenName = forms.CharField(label='givenName', max_length=30)
	CHOICES = (('200', 'eng'), ('300', 'app'), ('400', 'user'))
	gidNumber = forms.TypedChoiceField(choices=CHOICES)
	host = forms.CharField(label='hostname', widget=forms.Textarea(attrs={'cols': 20, 'rows': 10}), initial='bastion*,')

	def clean(self):
		form_data = self.cleaned_data
		if form_data['userPassword'] != form_data['confirm_userPassword']:
			self._errors["userPassword"] = ["Password do not match"]
			del form_data['userPassword']
		return form_data

class SetPasswordForm(forms.Form):
	new_password1 = forms.CharField(label=("New password"), widget=forms.PasswordInput)
	new_password2 = forms.CharField(label=("New password confirmation"), widget=forms.PasswordInput)

	def clean(self):
		form_data = self.cleaned_data
		if form_data['new_password1'] != form_data['new_password2']:
			self._errors["new_password2"] = ["Password do not match"]
			del form_data['new_password2']
			
		return form_data


class userPWForm(forms.Form):
	user_id = forms.CharField(label=("User ID"), max_length=254)