#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

from django.db import models
from django.conf import settings

__author__ = "tu"
__date__ = "$Mars 21, 2017 11:04:25 AM$"


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=256, default='')

    class Meta:
        db_table = 'vms_department'
