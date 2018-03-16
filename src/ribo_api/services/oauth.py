import httplib2
from googleapiclient import discovery
from oauth2client.client import OAuth2WebServerFlow

from ribo_api.services.api import ApiService
from ribo_api.services.base import BaseService
from oauth2client import client

from django.conf import settings


class OauthService(BaseService):

    @classmethod
    def _get_service(cls, access_token, user_agent):
        from ribo_api.services.user import UserService
        try:
            # oauth2 = ApiService.get_by_token(token=access_token)
            # user = UserService.get_user(oauth2.user_id)
            credentials = client.AccessTokenCredentials(access_token=access_token, user_agent=user_agent)
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)
            # service.owner_email = user.email
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

