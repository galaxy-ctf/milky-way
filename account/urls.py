from django.conf.urls import url, include
from rest_framework import routers
from account import views


router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
router.register(r'emailconfirmations', views.EmailConfirmationViewSet)
router.register(r'signupcoderesults', views.SignupCodeResultViewSet)
router.register(r'signupcodes', views.SignupCodeViewSet)
router.register(r'emailaddresses', views.EmailAddressViewSet)
router.register(r'accountdeletions', views.AccountDeletionViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
