from django.db import models

# when someone creates a post, you can have them sent back to another page
from django.urls import reverse

from django.conf import settings
import misaka

from groups.models import Group
from django.contrib.auth import get_user_model

# connects the current post to whoever is logged in as a user
User = get_user_model()


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete='CASCADE')
    # the time posted is auto-generated for you
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete='CASCADE')

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username,
                                               'pk': self.pk})

    class Meta:
        # in descending order
        ordering = ['-created_at']
        # every message is uniquely linked to a user
        unique_together = ['user', 'message']
