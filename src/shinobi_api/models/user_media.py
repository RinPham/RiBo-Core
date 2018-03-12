#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
from django.db import models
from django.conf import settings
from shinobi_api.models.timestamped import TimeStampedModel
from .usertypes import *

class UserMedia(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    origin_uri = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=10, default='')
    thumb_uri = models.CharField(max_length=255, default='')
    s3_name = models.CharField(max_length=255, default='')
    expires_at = models.IntegerField(default=0)
    
    origin_w = models.PositiveIntegerField(default=0)
    origin_h = models.PositiveIntegerField(default=0)
    thumb_w = models.PositiveIntegerField(default=0)
    thumb_h = models.PositiveIntegerField(default=0)
    on_remove = PositiveTinyIntegerField(default=0)
    class Meta:
        db_table = 'vms_user_medias'