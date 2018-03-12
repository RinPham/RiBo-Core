#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 05, 2016 2:29:54 PM$"

from shinobi_api.const import *
from shinobi_api.services.base import *
from shinobi_api.services.user import *
from shinobi_api.services.vmscache import *
from shinobi_api.models.loginlog import *
from shinobi_api.services.vmsrequest import *

class SecurityError(TypeError): pass  # base exception class

class VMSSecurityService(BaseService):
    MAX_TRY_FAILED = 3

    """
    vms_request: VMSRequest
    """
    @classmethod
    def log_login(cls, vms_request):
        user_id = vms_request.user_id
        ip_add = vms_request.ip
        user_agent = vms_request.user_agent
        response_code = vms_request.response_code
        filter_args = {
            'user_id': user_id,
            'ip': ip_add,
            'agent': user_agent
        }
        try:
            log_entry = LoginLog.objects.get(**filter_args)
            log_entry.tries +=1
        except Exception as e:
            log_entry = LoginLog()
            log_entry.user = UserService.get_user(user_id)
            log_entry.ip = ip_add
            log_entry.agent = user_agent
            log_entry.tries =1

        if (response_code is None) or (response_code != VMSRequest.RESPONSE_CODE_OK):
            log_entry.last_failed_at = int(time.time())
            if log_entry.tries>cls.MAX_TRY_FAILED:
                ##TODO: Log user temporary
                UserService.lock_user(user_id)
                pass
        log_entry.save()
        return log_entry