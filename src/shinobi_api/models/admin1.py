#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
from django.db import models


class Admin1(models.Model):
    id = models.AutoField(primary_key=True)
    country_code = models.CharField(max_length=2)
    admin1_code = models.CharField(max_length=5)
    admin1_name = models.CharField(max_length=64)
    timezone = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = 'vms_admin1'
