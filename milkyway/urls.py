from django.conf.urls import url, include
from milkyway import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        url(r'^$', views.index, name='index'),
        # ex: /chals/ - urls for pages needing to view chal model itself.
        url(r'^chals/$', views.ChalListView.as_view(), name='chal-list'),
        url(r'^chals/create/$', views.ChalCreate.as_view(), name='chal-create'),
        url(r'^chals/(?P<pk>[0-9]+)/$', views.ChalDetailView.as_view(), name='chal-detail'),
        url(r'^chals/(?P<pk>[0-9]+)/update/$', views.ChalUpdate.as_view(), name='chal-update'),
        url(r'^chals/(?P<pk>[0-9]+)/delete/$', views.ChalDelete.as_view(), name='chal-delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
