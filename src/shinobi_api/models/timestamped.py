#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__all__ = ['TimeStampedModel']

from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    #trung: could not set created_at if auto_now_add=True
    #https://docs.djangoproject.com/en/1.8/ref/models/fields/#django.db.models.DateField.auto_now_add
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        abstract = True