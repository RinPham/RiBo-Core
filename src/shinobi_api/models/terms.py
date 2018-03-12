#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.db import models
from django.utils import timezone


def clean_terms_content(content):
    return content


class Terms(models.Model):
    content = models.TextField('Terms')
    updated_at = models.DateTimeField('Updated at')

    def save(self, **kwargs):
        self.updated_at = timezone.now()
        self.content = clean_terms_content(self.content)
        return super(Terms, self).save(**kwargs)

    class Meta:
        db_table = 'vms_terms'
