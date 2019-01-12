from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', auth_views.login, {'template_name': 'AuthApp/login.html'}),
    url(r'^logout/$', auth_views.logout, {'template_name': 'AuthApp/logout.html'}),
    url(r'^register/$', views.register),
]