from django.conf.urls import url, include
from rest_framework import routers
from milkyway import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'solveses', views.SolvesViewSet)
router.register(r'flags', views.FlagViewSet)
router.register(r'challenges', views.ChallengeViewSet)

urlpatterns = [
    url(r'^milkyway/', include(router.urls)),
]