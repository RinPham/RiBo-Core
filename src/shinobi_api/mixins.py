#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "$Jul 05, 2016 04:15:00 PM$"

from rest_framework.response import Response
from rest_framework import status

from shinobi_api.serializers import UserSerializer, AppKeySerialiser
from shinobi_api.services.user import UserService
from shinobi_api.services.api import ApiService
from shinobi_api.services.auth import AppKeyService
from shinobi_api.views import BaseViewSet


class GenericViewMixin(BaseViewSet):
    service_class = None
    lookup_field = 'pk'
    lookup_url_kwarg = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_service_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `service_class` attribute, "
            "or override the `get_service_class()` method."
            % self.__class__.__name__
        )
        pass

    def get_service(self, *args):
        service_class = self.get_service_class()
        return service_class(*args)

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}


class UserLoginMixin(object):
    def response_login(self, id=None, user=None, key=None, *args, **kwargs):
        token = kwargs.pop('token', None)
        response_status = kwargs.pop('status', status.HTTP_200_OK)
        client = kwargs.pop('client', None)
        assert id is not None or user is not None, (
            'Please provide user id or user instance'
        )
        assert token is not None or client is not None, (
            'Please provide token or client instance'
        )
        if user is None:
            user = UserService.get_user(id)
        if token is None:
            remember_me = kwargs.pop('remember_me', False)
            token = ApiService.create_token(user, client, remember_me=remember_me)
        if not isinstance(token, str):
            token = token.token
        data = UserSerializer(user).data
        response_data = {
            'user': data,
            'token': token,
        }
        if key:
            response_data['appkey'] = AppKeySerialiser(AppKeyService.get(key)).data
        if kwargs.pop('return_response', True):
            return Response(response_data, status=response_status)
        else:
            return response_data

