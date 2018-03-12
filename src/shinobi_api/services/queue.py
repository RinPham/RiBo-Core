#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 25, 2016 11:49:18 AM$"

from shinobi_api.const import *
from shinobi_api.services.base import *
class QueueError(TypeError): pass  # base exception class
from shinobi_api.services.utils import Utils

class QueueService(BaseService):
    
    QUEUE_NAME_EMAIL = 'send_email';
    
    WORKERS = {
        QUEUE_NAME_EMAIL: "django_q.send_email"
    }
    
    """
    START django-q cluser
    
        python manage.py qcluster
    
    job name: Should be one of QUEUE name constant
    args: arguments for the job, could be a simple dict (no nest dict) because it using eval(string) to convert string back to dict
    delayed_time: deplay time
    """
    @classmethod
    def async_job(cls, job_name, fname, args, delayed_time = 0):
        try:
            # Async class instance example
            from django_q.tasks import Async
            # instantiate an async task
            a = Async(fname, args, group=job_name)
            # you can set or change keywords afterwards
            a.cached = True
            # run it
            a.run()
            return True
        except Exception as e:
            Utils.log_exception(e)
            return None
        

    
