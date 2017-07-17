from django.contrib import admin

from acl_poc.models import Business, User

admin.site.register(User)
admin.site.register(Business)
