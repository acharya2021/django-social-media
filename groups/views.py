from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
# import the CBVs
from django.views import generic
from .models import Group, GroupMember


# someone is logged in and wants to create their own group
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    # i want them to be able to edit these fields
    fields = ('name', 'description')
    # connect it to the actual model
    model = Group


# to display posts inside the group
class SingleGroup(generic.DetailView):
    model = Group


# a list of al the groups
class ListGroups(generic.ListView):
    model = Group
