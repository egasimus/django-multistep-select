from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

urlpatterns = patterns(
    '',

    url(r'', include('test_app.urls')),
)

urlpatterns += static(settings.STATIC_URL)
