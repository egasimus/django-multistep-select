from django.conf.urls import patterns, url
from .views import Home

urlpatterns = patterns(
    '',

    url(r'^$', Home.as_view(), name='home'),
)
