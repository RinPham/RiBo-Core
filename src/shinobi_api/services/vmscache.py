#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 05, 2016 4:18:50 PM$"

from django.core.cache import cache
from shinobi_api.services.base import *
from shinobi_api.services.utils import Utils
from shinobi_api.const import *

class CacheError(TypeError): pass  # base exception class


class VMSCacheService(BaseService):
    PREFIX = None

    @staticmethod
    def factory(resource_type):
        if resource_type == ResourceType.RS_USER: return _UserCache()
        elif resource_type == ResourceType.RS_APP: return _AppMetaCache()
        assert 0, "Bad cache creation: " + str(resource_type)

    def get_key(self, object_id):
        if object_id:
            return '_'.join([self.PREFIX, str(object_id)]);

    def set(self, object_id, object_value):
        object_key = self.get_key(object_id)
        return cache.set(object_key,object_value)

    def get(self, object_id):
        object_key = self.get_key(object_id)
        result = cache.get(object_key)
        return result

    def delete(self, object_id):
        object_key = self.get_key(object_id)
        return cache.delete(object_key)

    class Meta:
        abstract = True


class _UserCache(VMSCacheService):
    PREFIX = "vms_users"
    
class _AppMetaCache(VMSCacheService):
    PREFIX = "vms_metas"