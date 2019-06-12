from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
# import the CBVs
from django.views import generic
from . import models
from .models import Group, GroupMember

from django.shortcuts import get_object_or_404
from django.contrib import messages


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


class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # redirect to the detail view of that particular group
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    #     add checks in case this person is already a member of this group
    def get(self, request, *args, **kwargs):
        # try to get the object or return a 404
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            # grab a GroupMember object and create it with the user = current user
            # and group = group which is the group we created above the try statement
            GroupMember.objects.create(user=self.request.user, group=group)
        except:
            messages.warning(self.request, 'Warning already a member!')
        else:
            messages.success(self.request, 'You are now a member!')
        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # redirect to the detail view of that particular group
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    # make sure they can't accidentally leave a group they are not a part of
    def get(self, request, *args, **kwargs):
        try:
            # try to get a membership assuming that the user is already in that group
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        #     the GroupMember was never a member of that group
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, "Sorry you are not in this group!")
        else:
            membership.delete()
            messages.success(self.request, "You have left the group!")
        return super().get(request, *args, **kwargs)
