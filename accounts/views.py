from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import (CreateView,
                                  )

# connect forms for logging in or signing up to the views
# the forms will be injected into the templates through a context dict
from . import forms


# Create your views here.

# creating a user
class Signup(CreateView):
    # connect to a user create form
    form_class = forms.UserCreateForm
    # on a successful signup, reverse them back to the login page
    # lazy because don't execute until the submit button is hit
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
