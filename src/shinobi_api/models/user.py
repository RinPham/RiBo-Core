from __future__ import unicode_literals

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "07 07 2016, 10:01 AM"

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
    BaseUserManager
)
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from shinobi_api.const import UserType, USER_TYPE_CHOICES
from shinobi_api.models.usertypes import TinyIntegerField

def update_last_login(sender, user, **kwargs):
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])


user_logged_in.connect(update_last_login)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
        null=True,
        help_text=_('Required. 245 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True
    
    @property
    def full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()
    
    @property
    def short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    is_disabled = models.BooleanField(default=False)
    # manager_id = models.PositiveIntegerField(default=0)
    # user_type = TinyIntegerField(default=UserType.GUEST, choices=USER_TYPE_CHOICES)

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'

    # @property
    # def is_manager(self):
    #     if self.user_type and self.user_type == UserType.MANAGER:
    #         return True
    #     return False
    #
    # @property
    # def is_guest(self):
    #     if self.user_type and self.user_type == UserType.GUEST:
    #         return True
    #     return False

    def get_full_name(self):
        return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)

    def get_prev_login(self):
        from shinobi_api.models import LoginLog
        index = 0
        prev_login = None
        for record in LoginLog.objects.filter(user_id=self.id).order_by('-id')[:2]:
            if index == 1:
                prev_login = record.created_at
            index += 1
        return prev_login


    def __str__(self):
        return '{},{}'.format(
            self.first_name + self.last_name,
            self.email,
            # self.user_type,
            # self.manager_id
        )

