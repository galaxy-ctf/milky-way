from django.conf.urls import url, include
from milkyway import views

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^team/join_team/$', views.JoinTeamList.as_view(), name='join-team'),
        url(r'^chals/$', views.ChalListView.as_view(), name='chal-list'),
        url(r'^chals/(?P<pk>[0-9a-f-]+)/$', views.ChalDetailView.as_view(), name='chal-detail'),
        url(r'^cat/(?P<pk>[0-9a-f-]+)/$', views.CategoryDetailView.as_view(), name='cat-detail'),

        url(r"^scoreboard/$", views.TeamList.as_view(), name="scoreboard"),
        url(r"^team/$", views.TeamList.as_view(), name="team-list"),
        url(r"^team/(?P<pk>[0-9a-f-]+)/$", views.TeamDetail.as_view(), name="team-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
