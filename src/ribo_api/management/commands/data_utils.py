#! /usr/bin/python
from ribo_api.services.auth import AppKeyService

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__="hien"
__date__ ="$Jul 5, 2016 5:00:13 PM$"
from django.core.management.base import BaseCommand

from ribo_api.const import *
from django.db import connection
from subprocess import call
from os.path import dirname
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.six.moves import input
from ribo_api.services.utils import Utils

class Command(BaseCommand):
    help = 'Create test data'
    
    def add_arguments(self, parser):
        parser.add_argument('-reset_data',
            action='store_true',
            default=False,
            help='Clean system data')
        
        parser.add_argument('-set_pass',
            action='store_true',
            default=False,
            help='Set User pass')
        
    def _run_command(self,*args, **kwargs):
        BASE_DIR = dirname(dirname(dirname(dirname(__file__))))
        params = ["python", BASE_DIR+"/manage.py"]+args[0]
        return call(params)
    
    def _run_raw(self, query):
        cursor = connection.cursor()
        cursor.execute(query)
    
    def handle(self, *args, **options):
        from ribo_api.services.user import UserService
        
        password = input("Enter admin password: ")
        if password !='vms123':
            print ("Wrong pass")
            return
        if options.get('set_pass'):
            user_id = input("Enter user id: ")
            app_key = AppKeyService.get(user_id=user_id)
            if app_key:
                passwd = input("Enter pass: ")
                UserService.activate_user(dict(key=app_key.key, pin=passwd))
                print ("** Activated **")