from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns(
    '',

    url(r'^$', Home.as_view(), name='home'),
    url(r'^simple/$', SimpleFooCreate.as_view(), name='simple'),
    url(r'^simple/(?P<pk>\d+)/edit/$', SimpleFooUpdate.as_view(),
        name='simple_edit'),

    url(r'^filter/$', FilterBarCreate.as_view(), name='filter'),
    url(r'^filter/(?P<pk>\d+)/edit/$', FilterBarUpdate.as_view(),
        name='filter_edit'),

    url(r'^generic/$', GenericBazCreate.as_view(), name='generic'),
    url(r'^generic/(?P<pk>\d+)/edit/$', GenericBazUpdate.as_view(),
        name='generic_edit'),
)
