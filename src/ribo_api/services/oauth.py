import json

import httplib2
from googleapiclient import discovery
from oauth2client.client import OAuth2WebServerFlow

from ribo_api.exceptions import AuthenticationFailed
from ribo_api.services.api import ApiService
from ribo_api.services.base import BaseService
from oauth2client import client

from django.conf import settings


class OauthService(BaseService):

    @classmethod
    def check_access_token(cls, access_token):
        scope = 'https://www.googleapis.com/auth/calendar'
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
               % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
        scopes = result.get('scope').split(' ')
        if (result.get('error') is not None) or (scope not in scopes):
            raise AuthenticationFailed()
        else:
            return True

    @classmethod
    def _get_service(cls, token, service_name="calendar", version="v3"):
        try:
            oauth2 = ApiService.get_by_user(token)
            if oauth2:
                json = oauth2.json
                credentials = client.OAuth2Credentials.from_json(json)
            else:
                credentials = client.AccessTokenCredentials(token, '')
            http = credentials.authorize(httplib2.Http())
            service = discovery.build(service_name, version, http=http)
            return service
        except:
            return None

    @classmethod
    def get_flow(cls, redirect_uri):
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        scopes = ['https://www.googleapis.com/auth/userinfo.email',
                  'https://www.googleapis.com/auth/calendar',
                  'https://www.googleapis.com/auth/userinfo.profile']
        flow = OAuth2WebServerFlow(client_id, client_secret, scopes, redirect_uri=redirect_uri)
        flow.params['access_type'] = 'offline'
        flow.params['prompt'] = 'consent'
        return flow

    @classmethod
    def get_authorize_url(cls, redirect_uri):
        flow = cls.get_flow(redirect_uri)
        return flow.step1_get_authorize_url()

    @classmethod
    def get_credentials(cls, auth_code, redirect_uri):
        flow = cls.get_flow(redirect_uri)
        credentials = flow.step2_exchange(auth_code)
        return credentials

