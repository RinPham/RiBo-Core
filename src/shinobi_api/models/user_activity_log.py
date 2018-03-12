#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "07 28 2016, 9:10 AM"

import json

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from shinobi_api.models.usertypes import TinyIntegerField
from .usertypes import NormalTextField


class UserActivityLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    ip = models.GenericIPAddressField()
    action = models.CharField(_('Action'), max_length=6)
    status = models.SmallIntegerField(_('Request status code'), default=200)
    url = models.CharField(_('Url'), max_length=2000, default='')
    meta = NormalTextField(_('Meta data'), default='{}')
    created_at = models.DateTimeField(default=timezone.now)
    latest_at = models.DateTimeField(default=timezone.now)
    device_type = TinyIntegerField(default=0)
    
    @property
    def meta_json(self):
        if self.meta:
            return json.loads(self.meta)
        return {}

    class Meta:
        verbose_name = _('activity_log')
        verbose_name_plural = _('activity_logs')
        db_table = 'vms_user_activity_logs'
