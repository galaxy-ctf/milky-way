from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from milkyway.serializers import UserSerializer, GroupSerializer, SolvesSerializer, FlagSerializer, ChallengeSerializer
from milkyway.models import Solves, Flag, Challenge
from account.models import Account, Team
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import TemplateView
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect

# from django.conf import settings
# from django.contrib import messages
# from django.core.mail import send_mail
#from collection.forms import ContactForm
# from django import forms
from milkyway.forms import FlagForm, NewTeamForm, JoinTeamForm
import uuid


# renders the index page
def index(request):
    return render(request, 'milkyway/index.html', {})

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
        if 'form' not in kwargs:
            kwargs['form'] = FlagForm(dict(
                challenge_id=kwargs['object'].id,
                flag="",
            ))
        return super().get_context_data(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # Initialize form from POST data
        print(request.POST)
        if 'flag' in request.POST:
            data = {
                'challenge_id': self.object.id,
                'flag': '',
            }
            form = FlagForm(data)
            print(form.is_valid())
            if form.is_valid():
                # Success!
                messages.add_message(request, messages.SUCCESS, 'Success!')
                return self.render_to_response(context)
        else:
            form = FlagForm(dict(challenge_id=self.object.id))

        context['form'] = form
        return self.render_to_response(context)


# renders the list view that shows each chal
class ChalListView(ListView):
    model = Challenge
