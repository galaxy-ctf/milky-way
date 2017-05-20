from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from milkyway.serializers import UserSerializer, GroupSerializer, SolvesSerializer, FlagSerializer, ChallengeSerializer
from milkyway.models import Solves, Flag, Challenge
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
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
# from django.conf import settings
# from django.contrib import messages
# from django.core.mail import send_mail
#from collection.forms import ContactForm
# from django import forms
import uuid


# renders the index page
def index(request):
    return render(request, 'milkyway/index.html', {})

# renders detail view for each chal
class ChalDetailView(DetailView):
    model = Challenge

# renders the list view that shows each chal
class ChalListView(ListView):
    model = Challenge

# renders the create a chal page
class ChalCreate(CreateView):
    model = Challenge
    # selection of fields to show up on page
    fields = [
    'chal_name',
    'chal_picture',
    'short_description',
    'description',]

    def get_success_url(self):
        return reverse_lazy('website:chal-update',args=(self.object.id))


class ChalUpdate(UpdateView):
    model = Challenge
    # field selection
    fields = [
    'chal_name',
    'chal_picture',
    'short_description',
    'description',]
    template_name_suffix = '_update_form'

    # overwrite for_valid to ensure that the chal is saved with the correct owner id
    def form_valid(self, form):
       self.object = form.save(commit=False)
       self.object.chal_owner = self.request.user
       self.object.save()
       return super(ChalUpdate, self).form_valid(form)

    # overwrite post method to get the current chal and save the updated image to disk if it has been changed.
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        self.object = self.get_object()

        if form.is_valid():
            #print request.FILES
            if 'chal_picture' in request.FILES:
                newpic = request.FILES['chal_picture']
                # saving of image to disk happens here
                default_storage.save(uuid.uuid4().hex, ContentFile(newpic.read()))
        return super(ChalUpdate, self).post(request, *args, **kwargs)

# rendering of chal delete page
class ChalDelete(DeleteView):
    model = Challenge
    success_url = reverse_lazy('website:chal-list')
