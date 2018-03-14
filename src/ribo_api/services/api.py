from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model

from ribo_api.models import Api
from ribo_api.serializers.api import ApiSerializer
from ribo_api.services.base import *
from ribo_api.const import DeviceType
from ribo_api.services.utils import Utils

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
    if 'expire_time' in data:
        api_obj.expired_at = data['expire_time']
    return api_obj


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
        try:
            serializer = ApiSerializer(data = api_data)
            serializer.is_valid(raise_exception=True)
            return serializer.save()
        except Exception as e:
            raise e

    @classmethod
    def get_by_token(cls, token):
        """
        Get object by token
        :param token:
        :param ip: include ip in filter
        :exception Api.DoesNotExist
        :return object: Api
        """
        api_obj = Api.objects(access_token=token)
        return api_obj

    @classmethod
    def get_by_user(cls, user_id):
        """
        Get object by token
        :param token:
        :param ip: include ip in filter
        :exception Api.DoesNotExist
        :return object: Api
        """
        api_obj = Api.objects(user_id=user_id).order_by('-id')[0]
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
                Api.objects(access_token=token).delete()
                return True
            except:
                return False
        elif user_id:
            Api.objects(user_id=user_id).delete()
            return True
