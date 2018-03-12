#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.db import models
from django.utils import timezone


def clean_content(content):
    return content


class Privacy(models.Model):
    content = models.TextField('Privacy')
    updated_at = models.DateTimeField('Updated at')

    def save(self, **kwargs):
        self.updated_at = timezone.now()
        self.content = clean_content(self.content)
        return super(Privacy, self).save(**kwargs)

    class Meta:
        db_table = 'vms_privacy'
