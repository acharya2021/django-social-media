from django.db import models

# a lot of the authorization tools are built into django
# so you don't have to mess around with creating your own models for users
from django.contrib.auth import models


# Create your models here.
class User(models.User, models.PermissionsMixin):

    # if you want the string representation of a user, do the following
    # the username attribute comes built in with the User
    def __str__(self):
        return "@{}".format(self.username)
