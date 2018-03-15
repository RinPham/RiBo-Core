from ribo_api.services.base import BaseService
from ribo_api.services.oauth import OauthService


class EventService(BaseService):

    @classmethod
    def get_list(cls, access_token,user_agent):
        service = OauthService._get_service(access_token=access_token,user_agent=user_agent)
        events = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
        for _event in events:
            print(_event['title'])