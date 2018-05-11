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
    def render_event_str(cls, index, data, tz):
        str_reminder = False
        recurrence = data.get('recurrence', [])
        index = str(index)
        start_datetime = Utils.utc_to_local(datetime.strptime(data['start']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S'), tz)
        end_datetime = Utils.utc_to_local(datetime.strptime(data['end']['dateTime'][:-6], '%Y-%m-%dT%H:%M:%S'), tz)
        start_time = start_datetime.strftime('%I:%M %p')
        end_time = end_datetime.strftime('%I:%M %p')
        if not recurrence:
            if start_datetime.date() == end_datetime.date():
                str_reminder = MSG_STRING.EVENT_ITEM_NOREPEAT.format(str(index), data['summary'], start_time, end_time)
            else:
                str_reminder = MSG_STRING.EVENT_ITEM_NOREPEAT.format(str(index), data['summary'],
                                     start_datetime.strftime('%b %d, %Y at %I:%M %p'), end_time.strftime('%b %d, %Y at %I:%M %p'))
        elif 'FREQ=DAILY' in recurrence[0]:
            str_reminder = MSG_STRING.EVENT_ITEM_DAILY.format(str(index), data['summary'], start_time, end_time)
        elif 'FREQ=WEEKLY' in recurrence[0]:
            day_of_week = weekday_str[start_datetime.strftime('%a')]
            str_reminder = MSG_STRING.EVENT_ITEM_WEEKLY.format(str(index), data['summary'], start_time, end_time, day_of_week)
        elif 'BYDAY=MO,TU,WE,TH,FR' in recurrence[0]:
            str_reminder = MSG_STRING.EVENT_ITEM_WEEKDAYS.format(str(index), data['summary'], start_time, end_time)
        elif 'BYDAY=SU,SA' in recurrence[0]:
            str_reminder = MSG_STRING.EVENT_ITEM_WEEKENDS.format(str(index), data['summary'], start_time, end_time)
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
            str_reminder = MSG_STRING.EVENT_ITEM_MONTHLY.format(str(index), data['summary'], start_time, end_time, day_of_month)
        return str_reminder
