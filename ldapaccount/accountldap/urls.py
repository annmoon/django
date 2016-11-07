from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^users/$', views.userList, name='users'),
	url(r'^user-add/$', views.userAdd, name='user-add'),
	url(r'^login/$', auth_views.login, {'template_name': 'accountldap/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'accountldap/logout.html'}, name='logout'),
	url(r'^user-pw/$', views.userPWsend, name='user-pw'),
	url(r'^user-add-pw/(?P<uid>[0-9A-Za-z]+)-(?P<to_email>[0-9A-Za-z]+@[0-9A-Za-z]+)/$', views.userAddPWsend, name='user-add-pw'),
    url(r'^reset-user-pw/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.userPWreset, name='reset-user-pw'),
    url(r'^reset-user-confirm/$', views.userPWreset, name='reset-user-confirm'),
    #url(r'^reset_password', views.userPW, name="reset_password"),
]