#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
from django.db import models


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=64)
    currency = models.CharField(max_length=3, default='')

    class Meta:
        db_table = 'vms_countries'
