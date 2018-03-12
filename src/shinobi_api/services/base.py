#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 05, 2015 3:06:27 PM$"

import logging
from shinobi_api.const import *
from shinobi_api.services.utils import *
from django.db import connections

logger = logging.getLogger("project")

class BaseService:
    
    @staticmethod
    def last_query():
        print(connections['default'].queries)
                
    @classmethod
    def log_exception(cls, exc):
        logger.error(exc, exc_info=True)
        
    @classmethod
    def log_info(cls, message):
        logger.info(message)
    
    @classmethod
    def log_debug(cls, message):
        logger.debug(message)
        
    @classmethod
    def log(cls, message):
        logger.error(message)    
        
    class Meta:
        abstract = True