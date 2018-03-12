#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "03 10 2016, 2:52 PM"
__all__ = ['TokenAuthService', 'AppKeyService']

import hashlib
import datetime

from django.conf import settings
from django.core.cache import cache

from shinobi_api.models import User, AppKey
from shinobi_api.services.base import BaseService
from shinobi_api.services.utils import Utils

class BaseStorage(object):
    timeout = 3600

    def get(self, key):
        pass

    def set(self, key, val):
        pass

    def has(self, key):
        pass

    def delete(self, key):
        pass

    class Meta:
        abstract = True


class CacheStorage(BaseStorage):
    """
    Use cache to store one click password data
    """
    def get(self, key):
        return cache.get(key)

    def set(self, key, val, timeout):
        if not timeout:
            timeout = self.timeout
        return cache.set(key, val, timeout)

    def has(self, key):
        has = cache.get(key, None)
        if has is None:
            return False
        else:
            return True

    def delete(self, key):
        return cache.delete(key)


class RedisStorage(BaseStorage):
    client = None

    def __init__():
        pass

    def get(self, key):
        pass

    def set(self, key, val):
        pass

    def has(self, key):
        pass

    def delete(self, key):
        pass


class TokenAuthService(object):
    prefix = 'oct'
    token_prefix = 'S'
    storage = None

    @classmethod
    def get_storage(cls):
        if cls.storage is None:
            cls.storage = CacheStorage()
        return cls.storage

    @classmethod
    def save_token(cls, token, id, timeout=None):
        key = '_'.join([cls.prefix, cls.token_prefix + token])
        return cls.get_storage().set(key, id, timeout)

    @classmethod
    def gen_token(cls, user_id, timeout=60):
        """
        Generate 1click login token, default timeout is 60sec
        :param user_id: generate for this user id
        :param timeout: int, timeout in second
        :return:
        """
        now = datetime.datetime.now()
        text = settings.SECRET_KEY + str(user_id) + now.isoformat()
        # TODO: Upgrade hasher for token
        token = hashlib.md5(text).hexdigest()
        cls.save_token(token, id=user_id, timeout=timeout)
        return token

    @classmethod
    def check_token(cls, token, return_user=False):
        """
        Check current token is valid.
        Clear this token if a valid id has found.
        :param token:
        :param return_user: True if want to get a User object
        :return: False, Int user id or User object
        """
        key = '_'.join([cls.prefix, cls.token_prefix + token])
        storage = cls.get_storage()
        if storage.has(key):
            id = int(storage.get(key))
            storage.delete(key)
            if return_user and id:
                return User.objects.get(id=id)
            return id
        else:
            return False

KEY_SIZE = 20


class AppKeyService(BaseService):
    @classmethod
    def list(cls, user_id=None, **kwargs):
        """
        List app key
        :param user_id:
        :param kwargs: int limit, int offset, list filter
        :return:
        """

        limit = kwargs.get('limit', 20)
        offset = kwargs.get('offset', 0)
        end = offset + limit
        filter = kwargs.get('filter', {})
        if user_id:
            filter['user_id'] = user_id
        query = AppKey.objects.filter(**filter)[offset:end]
        count = AppKey.objects.filter(**filter).count()
        return {
            'result': query,
            'count': count
        }

    @classmethod
    def create(cls, data, **kwargs):
        """
        :param data: list (user_id)
        :return: AppKey object or false in case exception
        """
        try:
            appkey = AppKey.objects.get(user_id=data['user_id'])
            appkey.key = data.get('key') or cls._gen_key()
            appkey.save()
            return appkey
        except:
            appkey = AppKey.objects.create(
                user_id=data['user_id'],
                key=data.get('key') or cls._gen_key()
            )
            return appkey

    @classmethod
    def get(cls, key=None, user_id=0):
        """
        Get a key
        :param key:
        :return: AppKey object or None
        """
        try:
            if user_id:
                return AppKey.objects.get(user_id=user_id)
            return AppKey.objects.get(pk=key)
        except:
            return None

    @classmethod
    def _gen_key(cls, length=KEY_SIZE):
        key = Utils.id_generator(length)
        while AppKey.objects.filter(key=key).exists():
            key = Utils.id_generator(length)
        return key.upper()

    @classmethod
    def delete_all(cls, user_id):
        AppKey.objects.filter(user_id=user_id).delete()
