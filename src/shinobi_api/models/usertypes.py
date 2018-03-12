#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 05, 2016 11:04:25 AM$"
__all__ = ['TinyIntegerField', 'PositiveTinyIntegerField', 'NormalTextField']
from django.db import models


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class PositiveTinyIntegerField(models.PositiveSmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint unsigned"
        else:
            return super(PositiveTinyIntegerField, self).db_type(connection)


class NormalTextField(models.TextField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "text"
        else:
            return super(NormalTextField, self).db_type(connection)
