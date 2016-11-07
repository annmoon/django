from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ec2-list/$', views.get_ec2_search, name='get_ec2_search'),
    url(r'^ec2_list_test/$', views.get_ec2_search_test, name='get_ec2_search_test'),
    url(r'^sg-list/$', views.get_sg_list, name='get_sg_list'),
]