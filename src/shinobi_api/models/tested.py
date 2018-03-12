#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.db import models
from mongoengine import Document,fields

class Tested(Document):
    url = fields.StringField(required=True)
    dom = fields.StringField(required=True)
    apis = fields.ListField()
    testedElements = fields.ListField(required=False)
    version = fields.StringField(required=True)

    class Meta:
        app_label = 'no_sql'