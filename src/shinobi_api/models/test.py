#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.utils import timezone

from django.db import models
from mongoengine import *
from shinobi_api.models.page import Page


class Test(Document):
    os = models.CharField(max_length=100, default='Window 10')
    ram = models.IntegerField()
    tester = models.CharField(max_length=100)
    test_date = models.DateTimeField(auto_now_add=True)
    browser = models.CharField(max_length=100, default='Chrome')
    # page = EmbeddedDocumentField()

    class Meta:
        db_table = 'shinobi_test'
