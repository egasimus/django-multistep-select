from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',

    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^simple/$', views.SimpleFooCreate.as_view(), name='simple'),
    url(r'^filter/$', views.FilterBarCreate.as_view(), name='filter'),
    url(r'^generic/$', views.GenericBazCreate.as_view(), name='generic'),
)
