#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

from django.db import models
from shinobi_api.models.usertypes import TinyIntegerField

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=2)
    admin1_name = models.CharField(max_length=64)
    admin1_code = models.CharField(max_length=2, default='')
    city = models.CharField(max_length=64)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    weight = TinyIntegerField(default=0)
    
    def __str__(self):
        parts = []
        if self.city:
            parts.append(self.city)
            if self.admin1_code:
                parts.append(self.admin1_code)
        else:
            if self.admin1_name:
                parts.append(self.admin1_name)
        parts.append(self.country)
        return ", ".join(parts)

    class Meta:
        db_table = 'vms_locations'
