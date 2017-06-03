from django.conf.urls import url
from milkyway import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$'                          , views.index                                  , name='index')       ,
    url(r'^about/$'                    , views.about                                  , name='about')       ,
    url(r'^team/join_team/$'           , login_required(views.JoinTeamList.as_view()) , name='join-team')   ,
    url(r'^chals/$'                    , views.ChalListView.as_view()                 , name='chal-list')   ,
    url(r'^chals/(?P<pk>[0-9a-f-]+)/$' , views.ChalDetailView.as_view()               , name='chal-detail') ,
    url(r"^team/$"                     , views.TeamList.as_view()                     , name="team-list")   ,
    url(r"^team/(?P<pk>[0-9a-f-]+)/$"  , views.TeamDetail.as_view()                   , name="team-detail") ,
]
