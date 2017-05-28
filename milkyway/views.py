from account.models import Team
from milkyway.models import Solves, Challenge, Hint, Category

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from milkyway.forms import FlagForm, NewTeamForm, JoinTeamForm
import uuid


# renders the index page
def index(request):
    return render(request, 'milkyway/index.html', {})


def about(request):
    return render(request, 'milkyway/about.html', {})


class JoinTeamList(TemplateView):
    template_name = 'account/join_team.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form_new'] = NewTeamForm()
        context['form_join'] = JoinTeamForm()
        return context

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


class TeamList(ListView):
    model = Team

# renders detail view for each chal


class ChalDetailView(DetailView):
    model = Challenge

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FlagForm()
        context['is_solved'] = self.object.is_solved_by(self.request.user.account.team)
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

        return self.render_to_response(context)


class ChalListView(ListView):
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['completed'] = {
            s.challenge.id: True
            for s in Solves.objects.all().filter(team=self.request.user.account.team)
        }
        return context


class CategoryDetailView(DetailView):
    model = Category
