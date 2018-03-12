#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 5, 2016 9:17:18 AM$"
__all__ = ['BaseProfile', 'ManagerProfile', 'VisitorProfile', 'UserProfile']

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from datetime import date
from shinobi_api.const import (
    USER_TYPE_CHOICES, USER_GENDERS
)
from shinobi_api.models.usertypes import TinyIntegerField

class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    gender = TinyIntegerField(default=2, choices=USER_GENDERS)
    dob = models.DateField(_('Date of birth'), default=date.today)
    avatar = models.CharField(max_length=255, default='')
    msg_indicator = models.PositiveIntegerField(default=0)
    head_shot_media_id = models.PositiveIntegerField(default=0)
    NPI = models.PositiveIntegerField(null=True, unique=True, default=None)
    home_phonenumber = models.CharField('Home phone number', max_length=15, default='')
    mobile_phonenumber = models.CharField('Mobile phone number', max_length=15, default='')
    address1 = models.CharField(_('Address line 1'), max_length=255, default='')
    address2 = models.CharField(_('Address line 2'), max_length=255, default='')
    zip_code = models.CharField(_('Zipcode'), max_length=6, default='')
    city = models.CharField(_('City'), max_length=64, default='')
    location_id = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return "Id:{},T:{},G:{},D:{}".format(
            self.user.id or '',
            self.user.user_type or '',
            self.gender or '',
            self.dob or ''
        )

    class Meta:
        abstract = True


class ManagerProfile(models.Model):
    class Meta:
        abstract = True


class VisitorProfile(models.Model):
    class Meta:
        abstract = True


class UserProfile(BaseProfile):
    class Meta:
        db_table = 'vms_user_profiles'
