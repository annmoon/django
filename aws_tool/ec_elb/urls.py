from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^elb-list/$', views.get_elb, name='get_elb'),
]