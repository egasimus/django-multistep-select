from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',

    url(r'^$', views.Home.as_view(), name='home'),
    url(r'^foo/$', views.JustFooCreate.as_view(), name='foo'),
    url(r'^filter/$', views.FilterBarCreate.as_view(), name='filter'),
    url(r'^generic/$', views.GenericBazCreate.as_view(), name='generic'),
)
