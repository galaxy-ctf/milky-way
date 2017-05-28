import os
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    url(os.environ.get('DJANGO_URL_PREFIX', ''), include([
        url(r'', include('milkyway.urls')),
        url(r'', include('account.urls')),
        url(r'^admin/', admin.site.urls),
        # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ])),
]

# if settings.DEBUG:
    # import debug_toolbar
    # urlpatterns = [
                # url(r'^__debug__/', include(debug_toolbar.urls)),
    # ] + urlpatterns
