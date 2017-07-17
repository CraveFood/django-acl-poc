from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=16)

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


class User(AbstractBaseUser, PermissionsMixin):
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
