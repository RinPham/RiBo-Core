#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 05, 2016 12:45:00 PM$"

from django.db import models

class UserEmail(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.PositiveIntegerField(default=0)
    email = models.CharField(max_length=255, default='', unique=True)
    is_primary = models.BooleanField(default=0)
    token = models.CharField(max_length=40, default='')
    verified_at = models.PositiveIntegerField(default=0)
    created_at = models.PositiveIntegerField(default=1446015876)
    unsubscribe_at = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'vms_emails'