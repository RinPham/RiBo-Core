#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "08 23 2016, 10:41"

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class AppKey(models.Model):
    key = models.CharField(_("Token"), max_length=40, primary_key=True, serialize=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(_("Created"), auto_now_add=True)
    activated_at = models.DateTimeField(_("Actived at"), null=True)

    def save(self, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        return super(AppKey, self).save(**kwargs)

    def activate(self):
        if not self.activated_at:
            self.activated_at = timezone.now()
            self.save()
        return self.activated_at

    def is_activated(self):
        return True if self.activated_at else False

    class Meta:
        db_table = 'vms_app_keys'
