from django.db import models

# remove any chars that are not alphanumeric
from django.utils.text import slugify

# for link embedding, use markdown inside of posts
import misaka

# imports the user model currently active in this project
from django.contrib.auth import get_user_model

# call things off of the current user's session
User = get_user_model()

from django import template
from django.urls import reverse

# use custom template tags
register = template.Library()


# Create your models here.
class Group(models.Model):
    # I don't want groups to have overlapping group names
    name = models.CharField(max_length=255, unique=True)
    # no mistakes calling a url code, and group slugs don't overlap each other
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    # in case we want an html version of the description
    description_html = models.TextField(editable=False, default='', blank=True)
    # pass in a User object through the GroupMember class
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # whatever the name is, you can put spaces in it
        # so it will replace and lowercase things
        self.slug = slugify(self.name)
        # allows us to put markdown in there
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    # we want to link this class to both the user and the groups they belong to

    # a GroupMember can have membership to a Group
    group = models.ForeignKey(Group, related_name='memberships', on_delete='CASCADE')
    # we will have a user from above - the current user that's logged in
    # they're going to have some groups that they are a member of
    user = models.ForeignKey(User, related_name='user_groups', on_delete='CASCADE')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
