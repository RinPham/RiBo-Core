import json

import httplib2
from django.conf import settings
from django.core.management.base import BaseCommand
from oauth2client.client import AccessTokenCredentialsError

from ribo_api.const import *
from django.db import connection
from subprocess import call
from os.path import dirname
from django.contrib.auth import get_user_model

from ribo_api.exceptions import TokenExpired
from ribo_api.services.api import ApiService
from ribo_api.services.dialogflow import ApiAIService
from ribo_api.services.oauth import OauthService

User = get_user_model()
from ribo_api.services.utils import Utils

CLIENT_ID = '310203758762-vkc9hocnecbbcshsgf2ufctttp74pbgm.apps.googleusercontent.com'

class Command(BaseCommand):
    help = 'Create test data'
    
    def add_arguments(self, parser):
        parser.add_argument('-reset_data',
            action='store_true',
            default=False,
            help='Clean system data')

        parser.add_argument('-oauth',
            action='store_true',
            default=False,
            help='Oauth google')

        parser.add_argument('-get_event_list',
                            action='store_true',
                            default=False,
                            help='Get event list')

        parser.add_argument('-url_login',
                            action='store_true',
                            default=False,
                            help='get url login google')

        parser.add_argument('-create_token',
                            action='store_true',
                            default=False,
                            help='save token')

        parser.add_argument('-get_credential',
                            action='store_true',
                            default=False,
                            help='save token')

        parser.add_argument('-get_intent',
                            action='store_true',
                            default=False,
                            help='get intents')
        
    def _run_command(self,*args, **kwargs):
        BASE_DIR = dirname(dirname(dirname(dirname(__file__))))
        params = ["python", BASE_DIR+"/manage.py"]+args[0]
        return call(params)
    
    def _run_raw(self, query):
        cursor = connection.cursor()
        cursor.execute(query)
    
    def handle(self, *args, **options):

        if options.get('url_login'):
            redirect_uri = Utils.get_public_url('/api/v1/auth/get_auth_code')
            url = OauthService.get_authorize_url(redirect_uri)
            print(url)

        if options.get('oauth'):
            scope = 'https://www.googleapis.com/auth/calendar'
            access_token = input("Enter access token: ")
            # Check that the Access Token is valid.
            url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
                   % access_token)
            h = httplib2.Http()
            result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
            scopes = result.get('scope').split(' ')
            if result.get('error') is not None:
                print('Invalid Access Token.')
            elif scope not in scopes:
                print('Access Token not meant for this app.')
            else:
                print('Access Token is valid.')


        if options.get('get_event_list'):
            user_id = input("Enter user id: ")
            service = OauthService._get_service(user_id)
            try:
                items = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
                print(items)
            except AccessTokenCredentialsError as e:
                raise TokenExpired()
            except Exception as e:
                raise e

        if options.get('create_token'):
            json = input("Enter json: ")
            try:
                data = ApiService.create_token(json)
                print(data)
            except Exception as e:
                raise e

        if options.get('get_credential'):
            code = input('Enter authentication code: ')
            try:
                redirect_uri = Utils.get_public_url('/api/v1/auth/token')
                credentials = OauthService.get_credentials(code, redirect_uri)
                print(credentials)
            except Exception as e:
                pass

        if options.get('get_intent'):
            user_id = input('User_id:')
            while 1:
                text = input('Enter text: ')
                if text == '':
                    break
                try:
                    res = ApiAIService.get_response(user_id, text)
                    print(res['result']['fulfillment']['speech'])
                except Exception as e:
                    raise e
