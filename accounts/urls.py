from django.conf.urls import url
# as auth_views because you don't want to mix it up with original views
from django.contrib.auth import views as auth_views
from . import views

# for url templates in base.html, probably at nav bar
app_name = 'accounts'

urlpatterns = [
    # call LoginView from authorization view,
    # pass in the template we want it to connect to
    url(r'login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # will essentially go back to the hompage once you log out
    url(r'logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'signup/$', views.Signup.as_view(), name='signup'),
]
