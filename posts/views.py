from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views import generic
from django.http import Http404

from braces.views import SelectRelatedMixin
from . import models
from . import forms

from django.contrib.auth import get_user_model
from django.contrib import messages

# when someone is logged in, use this User as the current user and call things off of that
User = get_user_model()


# a list of posts belonging to a group
class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    # basically the foreign keys for this post
    # the user and the group that this post belongs to
    select_related = ('user', 'group')


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    # check whether the username is exactly equal to the username of whoever is logged in right now
    def get_queryset(self):
        try:
            # set the user that belongs to this particular post to
            # whatever username is exactly equal to the username of the user you click on
            # you want to fetch the posts that are related to the user
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    # grab the post user and return the context dict off of that
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        # return the context for the person who posted
        return context


# when you select a particular post, there is a detailed view on it
class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # fields I want someone to be able to edit
    fields = ('message', 'group')
    model = models.Post

    # connect the post to the user itself
    # check whether the form is valid
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    # once you delete a post, what is the success url
    # takes you back to all the posts
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    # a lot of these come with the CBV, good documentation
    # return something saying the post was deleted
    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
