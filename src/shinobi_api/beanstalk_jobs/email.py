#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 5, 2016 11:39:46 AM$"

from shinobi_api.services.utils import *
from shinobi_api.services.email import *
from django_beanstalkd import beanstalk_job

@beanstalk_job
def send_email(arg):
    try:
        Utils.log("SENDING EMAIL")
        Utils.log(arg)
        data = eval(arg)
        #data is a dict
        if not data:
            Utils.log(data)
            raise Exception('Bad params')
        EmailService._process_queue(data)
        Utils.log("DONE SENDING EMAIL")
    except Exception as e:
        Utils.log_exception(e)