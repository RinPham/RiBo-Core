from ribo_api.services.base import BaseService
from ribo_api.services.oauth import OauthService


class EventService(BaseService):

    @classmethod
    def get_list(cls, access_token,user_agent):
        service = OauthService._get_service(access_token=access_token,user_agent=user_agent)
        events = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
        for _event in events:
            print(_event['title'])

    @classmethod
    def create_event(cls, data):
        user_id = data.get('user_id', '')
        if user_id:
            service = OauthService._get_service(user_id)
            timezone = data.get("timezone", "Asia/Bangkok")
            event = {
                'summary': data.get('summary', None),
                'location': data.get('location', None),
                'description': data.get('description', None),
                'start': {
                    'dateTime': data.get('start_time', None),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': data.get('end_time', None),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
        return event