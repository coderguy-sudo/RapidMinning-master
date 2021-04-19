from django.conf.urls import url
from . import views

app_name = 'minning'

urlpatterns = [

    #main
    url(r'^$', views.IndexView.as_view(), name='index'),

    #registraion
    url(r'^registration/$', views.registration, name='registration'),

    #activate tokens
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

    #login
    url(r'^login/$', views.login_view, name='login'),

    #logout
    url(r'^logout/$', views.logout, name='logout'),

    #dashboard
    url(r'^dashboard/$', views.dashboard, name='dashboard'),

]

