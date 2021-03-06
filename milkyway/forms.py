from __future__ import unicode_literals

import re
from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from account.models import Team
from milkyway.models import Challenge



class FlagForm(forms.Form):
    flag = forms.CharField(label=_("Flag"), required=True, max_length=100)
    challenge_id = forms.CharField(required=True, max_length=100, widget=forms.HiddenInput())

    def clean(self):
        if self._errors:
            return

        chal = Challenge.objects.get(id=self.cleaned_data['challenge_id'])
        for flag in chal.flag_set.all():
            if flag.validate(self.cleaned_data['flag']):
                return

        raise forms.ValidationError("Incorrect")


class TeamForm(forms.Form):

    team = forms.CharField(label=_("Team Name"), required=True, max_length=128)
    password = forms.CharField(label=_("Team Passphrase"), required=True, max_length=128)

    def clean_team(self):
        value = self.cleaned_data["team"]
        print(value)
        if value in ('admin', 'galaxians', 'galaxy'):
            raise forms.ValidationError(_("These team names are not permitted."))
        print(value)
        return value


class NewTeamForm(TeamForm):
    def clean(self):
        if self._errors:
            return

        value = self.cleaned_data["team"]
        qs = Team.objects.filter(name__iexact=value)
        if not qs.exists():
            return
        raise forms.ValidationError(_("A team with that name already exists."))


class JoinTeamForm(TeamForm):
    def clean(self):
        if self._errors:
            return

        qs = Team.objects.filter(
            name=self.cleaned_data["team"],
            password=self.cleaned_data["password"]
        )
        if qs.exists():
            return

        raise forms.ValidationError("Unknown team")
