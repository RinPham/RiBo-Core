#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Oct 7th, 2016 9:17:18 AM$"
__all__ = ['AppMeta']

from django.db import models
from django.conf import settings
from shinobi_api.models.usertypes import TinyIntegerField
from shinobi_api.models.usertypes import NormalTextField


class AppMeta(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    version = models.CharField(max_length=10, default='v0.0.1')
    installed_at = models.DateTimeField(default=None, null=True)
    last_updated = models.DateTimeField(default=None, null=True)
    is_active = TinyIntegerField(default=1)

    def __str__(self):
        return "Version: {0}, Updated: {1}, Sensor: {2}".format(
            self.version or '',
            str(self.last_updated)
        )

    class Meta:
        db_table = 'vms_app_meta'
