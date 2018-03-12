#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 05, 2016 5:29:38 PM$"

import redis
from shinobi_api.services.base import *
from shinobi_api.const import *
from django.conf import settings

class RedisError(TypeError): pass  # base exception class

class VMSRedisService(BaseService):
    PREFIX = None
    client = None
    
    def __init__(self):
        self.client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    
    def flush_db(self):
        self.client.flushdb()