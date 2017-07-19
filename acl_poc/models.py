from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.query import EmptyQuerySet


class Business(PermissionsMixin, models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=16)
    is_active = models.BooleanField(default=True)

    @property
    def is_anonymous(self):
        return False

    class Meta:
        permissions = [
            ('list_business', 'Can list businesses'),
        ]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self.create_user(email, password, **kwargs)

    def get_by_natural_key(self, username):
        username = username.lower()
        return super().get_by_natural_key(username)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=50)
    business = models.ForeignKey('Business', related_name='users', null=True,
                                 on_delete=models.SET_NULL)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_username(self):
        return self.email.lower()

    def get_short_name(self):
        return self.get_full_name().split()[0]

    def get_full_name(self):
        return self.full_name or 'NO_NAME'

    @property
    def first_name(self):
        return self.full_name.split(' ')[0]

    @property
    def last_name(self):
        return self.full_name.split(' ')[-1]

    @property
    def groups(self):
        if not self.business:
            return EmptyQuerySet()
        return self.business.groups

    def has_perm(self, label):
        if self.is_staff:
            return True
        if not self.business:
            return False
        return self.business.has_perm(label)

    def has_module_perms(self, label):
        if self.is_staff:
            return True
        if not self.business:
            return False
        return self.business.has_module_perms(label)
