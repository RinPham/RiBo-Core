#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "$Jul 05, 2016 09:40:00 AM$"

from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from rest_framework import status, exceptions
from rest_framework.response import Response

from shinobi_api.mixins import UserLoginMixin
from shinobi_api.serializers import (
    UsernameAuthSerializer
)
from shinobi_api.services import (
    ApiService
)
from shinobi_api.views import BaseViewSet


def listener_login_failed(sender, credentials, **kwargs):
    """
    Do something with this credentials here when user login failed
    """
    # TODO:
    # Lock user
    # Last login failed
    pass


def listener_logged_in(sender, user=None, **kwargs):
    """
    Do something with this user here when user login success
    """
    pass


def listen_logged_out(sender, user=None, **kwargs):
    """
    Do something with user here when user logout
    """
    pass


user_login_failed.connect(listener_login_failed)
user_logged_in.connect(listener_logged_in)
user_logged_out.connect(listen_logged_out)


class AuthViewSet(BaseViewSet, UserLoginMixin):
    view_set = 'auth'
    serializer_class = UsernameAuthSerializer

    def create(self, request):
        """
        @apiVersion 1.0.0
        @api {post} /auth Login
        @apiName Authenticate
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {string} email Email address
        @apiParam {string} password Password
        @apiParam {Boolean} [remember_me] Remember me

        @apiSuccess {object} user User info
        @apiSuccess {string} token Token
        """
        auth_serializer = self.serializer_class(data=request.data)
        auth_serializer.is_valid(raise_exception=True)
        client = request.client
        remember_me = bool(request.data.get('remember_me', False))
        id = auth_serializer.validated_data['user'].pk
        return self.response_login(id=id, client=client, remember_me=remember_me)

    def delete(self, request):
        """
        @apiVersion 1.0.0
        @api {delete} /auth Logout
        @apiName Logout
        @apiGroup VMS_API Account
        @apiPermission authenticated

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Authenticated Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": "1",
            "Agent": "Samsung A5 2016, Android app, build_number other_info",
            "Authorization": "token QS7VF3JF29K22U1IY7LAYLNKRW66BNSWF9CH4BND"
        }

        @apiSuccess [200]
        """
        if request.user and request.user.is_authenticated():
            ApiService.delete_session(token=request.token)
            return Response(status=status.HTTP_200_OK)
        else:
            raise exceptions.NotAuthenticated()
