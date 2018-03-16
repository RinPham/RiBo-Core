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

    def get_authorize_url(redirect_uri):
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        scopes = ['https://www.googleapis.com/auth/userinfo.email',
                  'https://www.googleapis.com/auth/calendar']
        flow = OAuth2WebServerFlow(client_id, client_secret, scopes, redirect_uri=redirect_uri)
        flow.params['access_type'] = 'offline'
        flow.params['prompt'] = 'consent'
        return flow.step1_get_authorize_url()


if __name__ == '__main__':
    access_token = input('access token:')
    service = OauthService._get_service(access_token=access_token, user_agent='myAgent/2.0')
