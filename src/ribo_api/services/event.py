from ribo_api.const import weekday_str
from ribo_api.services.base import BaseService
from ribo_api.services.oauth import OauthService
from ribo_api.services.utils import Utils
from datetime import datetime

from ribo_api.string import MSG_STRING


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

    @classmethod
    def render_event_str(cls, data, tz):
        str_reminder = False
        recurrence = data.get('recurrence', [])
        start_datetime = datetime.strptime(data['start']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')
        end_datetime = datetime.strptime(data['end']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S')
        start_time = start_datetime.strftime('%I:%M %p')
        end_time = end_datetime.strftime('%I:%M %p')
        if not recurrence:
            if start_datetime.date() == end_datetime.date():
                str_reminder = MSG_STRING.EVENT_ITEM_NOREPEAT.format( data.get('summary', '(No title)'), start_time, end_datetime.strftime('%I:%M %p on %b %d, %Y'))
            else:
                str_reminder = MSG_STRING.EVENT_ITEM_NOREPEAT.format(data.get('summary', '(No title)'),
                                     start_datetime.strftime('%I:%M %p on %b %d, %Y'), end_datetime.strftime('%I:%M %p on %b %d, %Y'))
        elif 'FREQ=DAILY' in recurrence[0]:
            str_reminder = MSG_STRING.EVENT_ITEM_DAILY.format(data.get('summary', '(No title)'), start_time, end_time)
        elif 'FREQ=WEEKLY' in recurrence[0]:
            day_of_week = weekday_str[start_datetime.strftime('%a')]
            str_reminder = MSG_STRING.EVENT_ITEM_WEEKLY.format( data.get('summary', '(No title)'), start_time, end_time, day_of_week)
        elif 'BYDAY=MO,TU,WE,TH,FR' in recurrence[0]:
            str_reminder = MSG_STRING.EVENT_ITEM_WEEKDAYS.format(data.get('summary', '(No title)'), start_time, end_time)
        elif 'BYDAY=SU,SA' in recurrence[0]:
            str_reminder = MSG_STRING.EVENT_ITEM_WEEKENDS.format( data.get('summary', '(No title)'), start_time, end_time)
        elif 'FREQ=MONTHLY' in recurrence[0]:
            day_of_month = str(start_datetime.day)
            if day_of_month[-1] == '1':
                day_of_month = day_of_month + 'st'
            elif day_of_month[-1] == '2':
                day_of_month = day_of_month + 'nd'
            elif day_of_month[-1] == '3':
                day_of_month = day_of_month + 'rd'
            else:
                day_of_month = day_of_month + 'th'
            str_reminder = MSG_STRING.EVENT_ITEM_MONTHLY.format(data.get('summary', '(No title)'), start_time, end_time, day_of_month)
        return str_reminder
