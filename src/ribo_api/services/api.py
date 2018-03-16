import json

from django.contrib.auth import get_user_model

from ribo_api.models import Api
from ribo_api.serializers.api import ApiSerializer
from ribo_api.serializers.user import UserSerializer
from ribo_api.services.base import *
from ribo_api.services.user import UserService

User = get_user_model()

class ApiError(TypeError): pass  # base exception class


class ApiService(BaseService):
    @classmethod
    def create_token(cls, json_data, **kwargs):
        """
        Create a token object
        :param user_id:
        :param api_data:
        :param kwargs: save_log_login default True
        :param kwargs: remember_me default False only effects with browser
        :return:
        """
        try:
            api_data = {}
            data = json.loads(json_data)
            email = data['id_token'].get('email', None)
            user = UserService.get_user_by_email(email)
            if not user:
                data_user = {
                    'email': email,
                    'first_name': data['id_token'].get('given_name', None),
                    'last_name': data['id_token'].get('family_name', None),
                    'avatar': data['id_token'].get('picture', None),
                }
                user_serializer = UserSerializer(data=data_user)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()
            api_data['access_token'] = data.get('access_token','')
            api_data['refresh_token'] = data.get('refresh_token', '')
            api_data['json'] = json_data
            api_data['user_id'] = user.id
            serializer = ApiSerializer(data = api_data)
            serializer.is_valid(raise_exception=True)
            token = serializer.save()
            data = {
                'token': ApiSerializer(token).data,
                'user': UserSerializer(user).data
            }
            return data
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
