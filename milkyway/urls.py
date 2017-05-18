from django.conf.urls import url, include
from rest_framework import routers
from milkyway import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'assessments', views.AssessmentViewSet)
router.register(r'results', views.ResultViewSet)
router.register(r'iterations', views.IterationViewSet)
router.register(r'courses', views.CourseViewSet)

urlpatterns = [
    url(r'^milkyway/', include(router.urls)),
]