from django.contrib import admin
from discussions.models import Discussion
from discussions.models import Reply
# Register your models here.

admin.site.register(Discussion)
admin.site.register(Reply)