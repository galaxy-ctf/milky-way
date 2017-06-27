from account.models import Team
from milkyway.models import Solves, Challenge, Category

import datetime
import json
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.conf import settings
from django.utils import timezone
from milkyway.forms import FlagForm, NewTeamForm, JoinTeamForm
from cachetools import TTLCache

cache = TTLCache(
    1,  # Up to 1 items
    1 * 60  # 1 minute cache life
)


def add_dates(context):
    now = timezone.now()
    context['now'] = now
    context['COMPETITION_STARTS'] = settings.COMPETITION_STARTS
    context['COMPETITION_ENDS'] = settings.COMPETITION_ENDS
    context['competition_active'] = settings.COMPETITION_STARTS < now < settings.COMPETITION_ENDS
    return context

# renders the index page
def index(request):
    return render(request, 'milkyway/index.html', add_dates({}))


def about(request):
    return render(request, 'milkyway/about.html', {})


class JoinTeamList(TemplateView):
    template_name = 'account/join_team.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form_new'] = NewTeamForm()
        context['form_join'] = JoinTeamForm()
        return context

    def get(self, request, *args, **kwargs):
        # If they're already on a team, redirect them there.
        if request.user.account.team:
            return redirect(request.user.account.team)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(object_list=[])
        # Fill out the right form
        if request.POST['action'] == 'join':
            form = JoinTeamForm(request.POST)
            if form.is_valid():
                team = Team.objects.get(
                    name=form.cleaned_data['team'],
                    password=form.cleaned_data['password']
                )
                self.request.user.account.team = team
                self.request.user.account.save()
                return redirect(team)
            else:
                context['form_join'] = JoinTeamForm(request.POST)
        else:
            form = NewTeamForm(request.POST)
            if form.is_valid():
                team = Team.objects.create(
                    name=form.cleaned_data['team'],
                    password=form.cleaned_data['password']
                )
                self.request.user.account.team = team
                self.request.user.account.save()
                return redirect(team)
            else:
                context['form_new'] = NewTeamForm(request.POST)
        # Return response
        return self.render_to_response(context)


class TeamDetail(DetailView):
    model = Team

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context = add_dates(context)
        context['galaxy_username'] = self.object.name + '@galaxy.org'
        return context


class TeamList(ListView):
    model = Team

# renders detail view for each chal


class ChalDetailView(DetailView):
    model = Challenge

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FlagForm()
        context['is_solved'] = self.object.is_solved_by(self.request.user.account.team)
        context['hints'] = self.object.hint_set.all().filter(show=True)
        context = add_dates(context)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # Initialize form from POST data
        form = FlagForm(dict(challenge_id=self.object.id, flag=request.POST['flag']))
        context['form'] = form
        if 'flag' in request.POST:
            if form.is_valid():
                # Success!
                messages.add_message(request, messages.SUCCESS, 'Success!')
                Solves.objects.create(
                    challenge=self.object,
                    team=request.user.account.team,
                )
                # Override. This will be set properly NEXT time.
                context['is_solved'] = True

        return self.render_to_response(context)


class ChalListView(ListView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if not self.request.user.is_anonymous:
            context['completed'] = {
                s.challenge.id: True
                for s in Solves.objects.all().filter(team=self.request.user.account.team)
            }
        context = add_dates(context)
        return context

def admin_pw(request):
    client = request.META.get('HTTP_X_FORWARDED_FOR', 'x.x.x.x')
    clients = [c.strip() for c in client.split(',')]

    # If the data isn't available, load the freshest copy.
    if 'allowed_ips' not in cache:
        with open('/tmp/data.json', 'r') as handle:
            cache['allowed_ips'] = json.load(handle)

    # Set the admin PW if exists.
    admin_password = None
    for c in clients:
        if c in cache['allowed_ips']:
            admin_password = cache['allowed_ips'][c]
            break

    return render(request, 'milkyway/admin_pw.html', {'admin_pw': admin_password, 'ip': client})
