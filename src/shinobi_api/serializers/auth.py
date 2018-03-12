#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "Jul 05 2016, 11:14 AM"
__all__ = [
    'UsernameAuthSerializer', 'KeyPinAuthSerializer',
    'AppKeySerialiser', 'PinSeriaLiser'
]

import re

from django.contrib.auth import authenticate, user_logged_in, user_login_failed
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import serializers
from shinobi_api.models import AppKey
from shinobi_api.services.user import UserService


class AuthSerialiserMixin(object):
    def validate(self, attrs):
        for key in self.fields:
            if key not in attrs and self.fields[key].required:
                msg = _('Must include %s.' % (key,))
                raise exceptions.ValidationError(msg)
        user = authenticate(**attrs)
        if user:
            if not user.is_active:
                msg = _('User account is not activated.')
                raise exceptions.ValidationError(msg)
            if user.is_disabled:
                raise exceptions.ValidationError(_('Your account have been disabled.'))
        else:
            user_login_failed.send(sender=user.__class__, credentials=attrs)
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)
        user_logged_in.send(sender=user.__class__, user=user)
        attrs['user'] = user
        return attrs


class KeyPinAuthSerializer(AuthSerialiserMixin, serializers.Serializer):
    key = serializers.CharField(required=True)
    pin = serializers.CharField(required=False)

    def to_internal_value(self, data):
        data = super(KeyPinAuthSerializer, self).to_internal_value(data)
        if 'key' in data:
            data['key'] = re.sub('[^0-9a-zA-Z]+', '', data['key'])
            if data['key']:
                data['key'] = data['key'].upper()
        return data


class UsernameAuthSerializer(AuthSerialiserMixin, serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class AppKeySerialiser(serializers.ModelSerializer):
    class Meta:
        model = AppKey


class PinSeriaLiser(serializers.Serializer):
    key = serializers.CharField(required=True)
    pin = serializers.CharField(required=True)

    def validate(self, attrs):
        return UserService.activate_user(attrs)
