from django.contrib import admin
from .models import Account, EmailConfirmation, SignupCodeResult, SignupCode, EmailAddress, AccountDeletion

class AccountAdmin(admin.ModelAdmin):
    queryset = Account.objects.all()
    list_display = ('id', 'phone_number', 'name', 'language', 'netid', 'theme', 'original_id', 'user', 'orcid', 'timezone', 'nickname', 'initials',)

class EmailConfirmationAdmin(admin.ModelAdmin):
    queryset = EmailConfirmation.objects.all()
    list_display = ('id', 'created', 'objects', 'key', 'email_address', 'sent',)

class SignupCodeResultAdmin(admin.ModelAdmin):
    queryset = SignupCodeResult.objects.all()
    list_display = ('id', 'timestamp', 'signup_code', 'user', )

class SignupCodeAdmin(admin.ModelAdmin):
    queryset = SignupCode.objects.all()
    list_display = ('id', 'code', 'created', 'notes', 'expiry', 'use_count', 'max_uses', 'inviter', 'email', 'sent',)

class EmailAddressAdmin(admin.ModelAdmin):
    queryset = EmailAddress.objects.all()

class AccountDeletionAdmin(admin.ModelAdmin):
    queryset = AccountDeletion.objects.all()
    list_display = ('id', 'date_requested', 'user', 'date_expunged', 'email',)

admin.site.register(Account, AccountAdmin)
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
admin.site.register(SignupCodeResult, SignupCodeResultAdmin)
admin.site.register(SignupCode, SignupCodeAdmin)
admin.site.register(EmailAddress, EmailAddressAdmin)
admin.site.register(AccountDeletion, AccountDeletionAdmin)
