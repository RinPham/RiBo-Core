#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 05, 2016 09:16:54 AM$"

from rest_framework import exceptions, status
from django.utils.translation import ugettext_lazy as _


class BadHeaderParams(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid request headers')


class TokenExpired(exceptions.APIException):
    status_code = 432
    default_detail = _('Token expired')


class AuthenticationFailed(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Incorrect authentication credentials.')


class Gone(exceptions.APIException):
    status_code = 410
    default_detail = _('Gone')
