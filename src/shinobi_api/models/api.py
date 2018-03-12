#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#

from django.db import models
from django.conf import settings

from shinobi_api.models.timestamped import TimeStampedModel
from shinobi_api.models.usertypes import PositiveTinyIntegerField


class Api(TimeStampedModel):
    expired_at = models.DateTimeField(auto_now=False, default=settings.REST_FRAMEWORK['EXPIRED_FOREVER'])
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    device = models.CharField(max_length=64)
    ip = models.GenericIPAddressField()
    token = models.CharField(max_length=255)
    version = models.CharField(max_length=40)
    type = PositiveTinyIntegerField(default=0)
    app_id = models.CharField(max_length=64, default='')

    class Meta:
        db_table = 'vms_apis'
