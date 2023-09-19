from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, UserManager, PermissionsMixin)
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.


USER_MODEL = settings.AUTH_USER_MODEL


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        null=True,
        blank=True)
    first_name = models.CharField(
        _('First Name'),
        max_length=30,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=30,
        null=True,
        blank=True
    )
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        error_messages={
            'unique': _('User with that email already exists.')
        },
        null=True,
        blank=True
    )
    position = models.CharField(
        _("Employee Position"),
        max_length=150,
        choices=[
            ('Engineer', _('Engineer')),
            ('Manager', _('Manager'))
        ],
        default='Engineer'
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )
    USERNAME_FIELD = 'username'
    objects = UserManager()

    class Meta():
        verbose_name = _('user')
        verbose_name_plural = _('users')

User = MyUser()