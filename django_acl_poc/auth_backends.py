from django.apps import apps
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission


class BusinessBackend(ModelBackend):
    def _get_group_permissions(self, obj):
        groups_field = apps.get_model('acl_poc',
                                      'Business')._meta.get_field('groups')
        groups_query = 'group__%s' % groups_field.related_query_name()
        return Permission.objects.filter(**{groups_query: obj})
