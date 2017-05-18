from rest_framework import viewsets

from account.serializers import AccountSerializer, EmailConfirmationSerializer, \
    SignupCodeResultSerializer, SignupCodeSerializer, EmailAddressSerializer, \
    AccountDeletionSerializer, AccountSerializerLight
from account.models import Account, EmailConfirmation, SignupCodeResult, SignupCode, EmailAddress, AccountDeletion
import django_filters


class AccountFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_expr="icontains")
    email = django_filters.CharFilter(name="email", lookup_expr="icontains")

    class Meta:
        model = Account
        fields = ['name', 'id', 'email']


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    filter_class = AccountFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return AccountSerializerLight

        return AccountSerializer


class EmailConfirmationViewSet(viewsets.ModelViewSet):
    queryset = EmailConfirmation.objects.all()
    serializer_class = EmailConfirmationSerializer


class SignupCodeResultViewSet(viewsets.ModelViewSet):
    queryset = SignupCodeResult.objects.all()
    serializer_class = SignupCodeResultSerializer


class SignupCodeViewSet(viewsets.ModelViewSet):
    queryset = SignupCode.objects.all()
    serializer_class = SignupCodeSerializer


class EmailAddressViewSet(viewsets.ModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer


class AccountDeletionViewSet(viewsets.ModelViewSet):
    queryset = AccountDeletion.objects.all()
    serializer_class = AccountDeletionSerializer
