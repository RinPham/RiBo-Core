from datetime import datetime
from django.conf import settings
from django.utils import timezone
from rest_framework import authentication, HTTP_HEADER_ENCODING
from django.utils.translation import ugettext_lazy as _
from ribo_api.exceptions import (BadHeaderParams, TokenExpired, AuthenticationFailed)
from ribo_api.models.api import Api
from ribo_api.models.user import User


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
            token = self.model.objects(token=key)[0]
            user = User.objects(id=token.user_id)[0]
        except Exception as e:
            raise AuthenticationFailed(_('Invalid request token.'))

        if self.token_expired(token):
            # token.delete()
            raise TokenExpired()

        setattr(request, 'token', token.token)
        return (user, token)

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
        if token.expire_time == forever:
            return False
        now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        return token.expire_time < now