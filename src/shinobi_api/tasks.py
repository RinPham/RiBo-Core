#! /usr/bin/python
# django-q tasks define here

__author__ = "hien"
__date__ = "$Jul 25, 2016 3:37:49 PM$"

from shinobi_api.services.utils import Utils
from django.conf import settings


def send_email(*args, **kwargs):
    try:
        from shinobi_api.services.email import EmailService
        EmailService.sm_do_send(**args[0])
    except Exception as e:
        print("Unable to sending email: " + str(e))
        Utils.log_exception(e)
