from django.contrib import admin
from . import models


# Register your models here.

# ability to edit the model at the same level as the parent model
# when you visit Group inside admin, you want to edit GroupMembers as well
class GroupMemberInLine(admin.TabularInline):
    # the GroupMember model is inline here
    model = models.GroupMember


admin.site.register(models.Group)
