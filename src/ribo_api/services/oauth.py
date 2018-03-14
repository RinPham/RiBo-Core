import httplib2
from googleapiclient import discovery

from ribo_api.services.api import ApiService
from ribo_api.services.base import BaseService
from oauth2client import client

class OauthService(BaseService):

    @classmethod
    def _get_service(cls, access_token, user_agent):
        from ribo_api.services.user import UserService
        try:
            oauth2 = ApiService.get_by_token(token=access_token)
            user = UserService.get_user(oauth2.user_id)
            credentials = client.AccessTokenCredentials(access_token=access_token, user_agent=user_agent)
            http = credentials.authorize(httplib2.Http())
            service = discovery.build('calendar', 'v3', http=http)
            service.owner_email = user.email
            return service
        except:
            return None