#! /usr/bin/python
from MySQLdb.times import TimeDelta
from django.utils import timezone

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Sep 7, 2015 3:39:54 PM$"

from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model

from shinobi_api.models import Api, LoginLog
from shinobi_api.services.base import *
from shinobi_api.const import DeviceType

User = get_user_model()


class ApiError(TypeError): pass  # base exception class


def is_browser(type):
    return type == DeviceType.DESKTOP_WEB or type == DeviceType.MOBILE_WEB


def is_mobile_app(type):
    return not is_browser(type)


def set_client_data(api_obj, data):
    for key in ['device', 'ip', 'app_id', 'version', 'type']:
        setattr(api_obj, key, data.get(key))
    if 'user_id' in data:
        api_obj.user = data['user_id']
    if 'expired_at' in data:
        api_obj.expired_at = data['expired_at']
    return api_obj


DEFAULT_TOKEN_LENGTH = 40


class ApiService(BaseService):
    @classmethod
    def create_token(cls, user_id, api_data, **kwargs):
        """
        Create a token object
        :param user_id:
        :param api_data:
        :param kwargs: save_log_login default True
        :param kwargs: remember_me default False only effects with browser
        :return:
        """
        api_data['type'] = int(api_data['type'])
        api_data['user_id'] = user_id
        api_obj = None
        save_log_login = kwargs.get('save_login_log', True)
        token_length = kwargs.get('token_length', DEFAULT_TOKEN_LENGTH)
        if is_browser(api_data['type']):
            remember_me = kwargs.get('remember_me', False)
            now = datetime.now()
            if remember_me:
                expired = now + timedelta(30, 0)
            else:
                expired = now + timedelta(2, 0)
            api_data['expired_at'] = expired
            api_obj = cls._create(api_data, token_length)
        else:
            try:
                api_obj = Api.objects.get(device=api_data['device'], type=api_data['type'])
                api_obj.token = cls._gen_unique_str()
                api_obj = set_client_data(api_obj, api_data)
                api_obj.save()
            except Api.DoesNotExist:
                api_data['expired_at'] = settings.REST_FRAMEWORK['EXPIRED_FOREVER']
                api_obj = cls._create(api_data, token_length)
        if save_log_login:
            api_data['id'] = api_obj.id
            cls.log_login(**api_data)
        return api_obj

    @classmethod
    def _create(cls, data, token_length=DEFAULT_TOKEN_LENGTH):
        api_obj = Api()
        api_obj.token = cls._gen_unique_str(token_length)
        api_obj = set_client_data(api_obj, data)
        api_obj.save()
        return api_obj

    @classmethod
    def log_login(cls, **kwargs):
        user_id = kwargs['user_id']
        if not isinstance(user_id, int):
            user_id = user_id.id
        last = LoginLog.objects.order_by('-id').filter(user_id=user_id).first()
        time_since_last_login = 0
        time_since_last_open_app = 0
        if last:
            time_since_last_login = (timezone.now() - last.created_at).total_seconds()
            time_since_last_open_app = time_since_last_login
        return LoginLog.objects.create(
            user_id=user_id,
            api_id=kwargs['id'],
            ip=kwargs['ip'],
            user_agent=kwargs['user_agent'],
            device_id=kwargs.get('device', ''),
            time_since_last_login=time_since_last_login,
            time_since_last_open_app=time_since_last_open_app
        )

    @classmethod
    def _gen_unique_str(cls, length=DEFAULT_TOKEN_LENGTH):
        str = Utils.id_generator(length)
        if length < 40:
            while Api.objects.filter(token=str).exists():
                str = Utils.id_generator(length)
        return str


    @classmethod
    def get_by_token(cls, token, ip=None):
        """
        Get object by token
        :param token:
        :param ip: include ip in filter
        :exception Api.DoesNotExist
        :return object: Api
        """
        if not ip:
            api_obj = Api.objects.get(token=token)
        else:
            api_obj = Api.objects.get(token=token, ip=ip)
        return api_obj

    @classmethod
    def delete_session(cls, token=None, user_id=None):
        """
        Delete a token session by token or by user_id
        :param token:
        :return: boolean
        """
        if token:
            try:
                Api.objects.get(token=token).delete()
                return True
            except:
                return False
        elif user_id:
            Api.objects.filter(user_id=user_id).delete()
            return True
