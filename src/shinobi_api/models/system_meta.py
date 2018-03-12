#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "$Oct 7th, 2016 9:17:18 AM$"
__all__ = ['SystemMeta']

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from shinobi_api.models.usertypes import TinyIntegerField
from shinobi_api.models.usertypes import NormalTextField
from django.utils import timezone
from shinobi_api.models.timestamped import TimeStampedModel

class SystemMeta(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=10, default='v0.0.1')
    version_name = models.CharField(max_length=50, default='VMS v0.0.1')
    changes = NormalTextField(default=None)
    available_at = models.DateTimeField(default=None,null=True)
    is_latest = TinyIntegerField(default=1)
    is_force_updated = TinyIntegerField(default=0)
    
    def __str__(self):
        return "Version: {0}, Updated: {1}".format(
            self.version or '',
            str(self.updated_at)
        )

    class Meta:
        db_table = 'vms_system_meta'
        ordering = ['-id']
