import waffle
from restless.dj import DjangoResource
from restless.exceptions import Forbidden
from restless.preparers import FieldsPreparer

from acl_poc.models import Business

FEATURE_NOT_ALLOWED = 'User not allowed to access this feature'
RESOURCE_NOT_ALLOWED = 'User not allowed to access this resource'


def require_permission(*permissions):
    def validate_business(fn):
        def validate(self, *args, **kwargs):
            if not self.request.user.is_authenticated:
                raise Forbidden('User not logged in')
            if not any([self.request.user.has_perm(permission)
                        for permission in permissions]):
                raise Forbidden(RESOURCE_NOT_ALLOWED)
            return fn(self, *args, **kwargs)
        return validate
    return validate_business


class BusinessResource(DjangoResource):
    require_feature = 'business'
    preparer = FieldsPreparer({
        'id': 'id',
        'name': 'name',
        'type': 'type',
    })

    def handle(self, endpoint, *args, **kwargs):
        if getattr(self, 'require_feature') and not \
                waffle.flag_is_active(self.request, self.require_feature):
            return self.build_error(Forbidden(FEATURE_NOT_ALLOWED))
        return super().handle(endpoint, *args, **kwargs)

    @require_permission('acl_poc.list_business')
    def list(self, *args, **kwargs):
        return Business.objects.all()
