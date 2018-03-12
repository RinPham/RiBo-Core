#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
from django.db import models

class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    short = models.CharField(max_length=2)
    
    class Meta:
        db_table = 'vms_languages'