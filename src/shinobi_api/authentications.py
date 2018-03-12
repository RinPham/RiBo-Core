#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 5, 2016 09:30:54 AM$"

from datetime import datetime
from django.conf import settings
from django.contrib.auth import backends, get_user_model
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import authentication, HTTP_HEADER_ENCODING
from shinobi_api.exceptions import (BadHeaderParams, TokenExpired, AuthenticationFailed)
from shinobi_api.models.api import Api
from shinobi_api.services import AppKeyService


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class TokenAuthentication(authentication.BaseAuthentication):
    """
    Custom token authentication
    """
    model = Api

    def authenticate(self, request):

        self._check_headers(request)
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, key, request):
        try:
            token = self.model.objects.select_related('user').get(token=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid request token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        if self.token_expired(token):
            # token.delete()
            raise TokenExpired()

        setattr(request, 'token', token.token)
        return (token.user, token)

    def _check_headers(self, request):
        if hasattr(request, 'bad_request_header'):
            raise BadHeaderParams()

    def token_expired(self, token):
        """
        Check token timeout
        :param token:
        :return: boolean
        """
        forever = timezone.make_aware(
            datetime.strptime(settings.REST_FRAMEWORK['EXPIRED_FOREVER'], '%Y-%m-%d %H:%M:%S'))
        if token.expired_at == forever:
            return False
        now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        return token.expired_at < now


class KeyPinBackend(backends.ModelBackend):
    """
    Custom authentication method by token and pin
    """

    def _reset_stats(self, key):
        get_user_model()().set_password(key)

    def authenticate(self, key=None, pin=None, **kwargs):
        if key:
            appkey = AppKeyService.get(key)
            if appkey is None:
                return self._reset_stats(key)
            user = appkey.user
            user.key = appkey.key
            # Pin has provided and this pin is actived, should check pin
            if appkey.activated_at:
                if pin and user.check_password(pin):
                    return user
                return self._reset_stats(key)
            return user
