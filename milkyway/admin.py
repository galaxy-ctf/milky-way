from django.contrib import admin
from .models import Solves, Flag, Challenge

class SolvesAdmin(admin.ModelAdmin):
    queryset = Solves.objects.all()
    list_display = ('id', 'challenge', 'team',)

class FlagAdmin(admin.ModelAdmin):
    queryset = Flag.objects.all()
    list_display = ('id', 'flag_is_regex', 'flags', 'chal',)

class ChallengeAdmin(admin.ModelAdmin):
    queryset = Challenge.objects.all()
    list_display = ('category', 'name', 'value', 'id', 'description', 'hidden',)

admin.site.register(Solves, SolvesAdmin)
admin.site.register(Flag, FlagAdmin)
admin.site.register(Challenge, ChallengeAdmin)
