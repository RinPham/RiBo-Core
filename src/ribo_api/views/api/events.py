from rest_framework import status
from oauth2client.client import AccessTokenCredentialsError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api import permissions
from ribo_api.exceptions import TokenExpired
from ribo_api.models.task import Task
from ribo_api.models.user import User
from ribo_api.serializers.event import EventSerializer
from ribo_api.services.oauth import OauthService
from ribo_api.services.utils import Utils


class EventViewSet(ViewSet):
    view_set = 'event'
    serializer_class = EventSerializer

    def list(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /event Get event list
        @apiName EventList
        @apiGroup Ribo_api Event
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiSuccess {object} event
        @apiSuccessExample {json}
        {
            "kind": "calendar#events",
            "updated": "2018-03-18T09:28:21.270Z",
            "etag": "\"p33oanr5iovqti0g\"",
            "summary": "thqbop@gmail.com",
            "items": [
                {
                    "kind": "calendar#event",
                    "creator": {
                        "email": "thqbop1@gmail.com"
                    },
                    "iCalUID": "24m6ps5v1vtardfihidsb1nsig@google.com",
                    "reminders": {
                        "useDefault": true
                    },
                    "attachments": [
                        {
                            "title": "IMG_2726.JPG",
                            "iconLink": "https://ssl.gstatic.com/docs/doclist/images/icon_10_generic_list.png",
                            "fileId": "1SOkB6uHsdfXmn2oY31D5g0t_0P6Wqzn1",
                            "fileUrl": "https://drive.google.com/file/d/1SOkB6uHsdfXmn2oY31D5g0t_0P6Wqzn1/view?usp=drive_web"
                        }
                    ],
                    "etag": "\"3042179875790000\"",
                    "summary": "Abc222",
                    "attendees": [
                        {
                            "self": true,
                            "displayName": "Hàn Quốc Trương",
                            "responseStatus": "accepted",
                            "email": "thqbop@gmail.com"
                        },
                        {
                            "organizer": true,
                            "responseStatus": "accepted",
                            "email": "thqbop1@gmail.com"
                        }
                    ],
                    "status": "confirmed",
                    "end": {
                        "dateTime": "2018-03-12T14:00:00+07:00"
                    },
                    "updated": "2018-03-15T04:58:57.895Z",
                    "sequence": 0,
                    "htmlLink": "https://www.google.com/calendar/event?eid=MjRtNnBzNXYxdnRhcmRmaWhpZHNiMW5zaWcgdGhxYm9wQG0",
                    "start": {
                        "dateTime": "2018-03-12T11:30:00+07:00"
                    },
                    "created": "2018-03-15T04:16:32.000Z",
                    "organizer": {
                        "email": "thqbop1@gmail.com"
                    },
                    "id": "24m6ps5v1vtardfihidsb1nsig"
                },
            ],
            "accessRole": "owner",
            "timeZone": "Asia/Saigon",
            "defaultReminders": [
                {
                    "method": "popup",
                    "minutes": 30
                }
            ]
        }
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            items = service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute()
            return Response(items)
        except AccessTokenCredentialsError as e:
            raise TokenExpired()
        except Exception as e:
            raise e

    def create(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /event Create event
        @apiName EventCreate
        @apiGroup Ribo_api Event
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiParam {string} summary title event
        @apiParam {string} description
        @apiParam {string} location
        @apiParam {datetime} start_time format '2018-03-18T09:00:00+07:00'
        @apiParam {datetime} end_time format '2018-03-18T09:00:00+07:00'
        ....

        @apiSuccess {object} event
        @apiSuccessExample {json}
        {
            "kind": "calendar#event",
            "creator": {
                "email": "thqbop1@gmail.com"
            },
            "iCalUID": "24m6ps5v1vtardfihidsb1nsig@google.com",
            "reminders": {
                "useDefault": true
            },
            "attachments": [
                {
                    "title": "IMG_2726.JPG",
                    "iconLink": "https://ssl.gstatic.com/docs/doclist/images/icon_10_generic_list.png",
                    "fileId": "1SOkB6uHsdfXmn2oY31D5g0t_0P6Wqzn1",
                    "fileUrl": "https://drive.google.com/file/d/1SOkB6uHsdfXmn2oY31D5g0t_0P6Wqzn1/view?usp=drive_web"
                }
            ],
            "etag": "\"3042179875790000\"",
            "summary": "Abc222",
            "attendees": [
                {
                    "self": true,
                    "displayName": "Hàn Quốc Trương",
                    "responseStatus": "accepted",
                    "email": "thqbop@gmail.com"
                },
                {
                    "organizer": true,
                    "responseStatus": "accepted",
                    "email": "thqbop1@gmail.com"
                }
            ],
            "status": "confirmed",
            "end": {
                "dateTime": "2018-03-12T14:00:00+07:00"
            },
            "updated": "2018-03-15T04:58:57.895Z",
            "sequence": 0,
            "htmlLink": "https://www.google.com/calendar/event?eid=MjRtNnBzNXYxdnRhcmRmaWhpZHNiMW5zaWcgdGhxYm9wQG0",
            "start": {
                "dateTime": "2018-03-12T11:30:00+07:00"
            },
            "created": "2018-03-15T04:16:32.000Z",
            "organizer": {
                "email": "thqbop1@gmail.com"
            },
            "id": "24m6ps5v1vtardfihidsb1nsig"
        }
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            data = request.data.copy()
            timezone = data.get("timezone", "UTC")
            event = {
                'summary': data.get('summary',None),
                'location': data.get('location',None),
                'description': data.get('description',None),
                'start': {
                    'dateTime': data.get('start_time',None),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': data.get('end_time',None),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            return Response(event)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def update(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /event/:id Edit event
        @apiName EventEdit
        @apiGroup Ribo_api Event
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiParam {string} summary title event
        @apiParam {string} description
        @apiParam {string} location
        @apiParam {datetime} start_time format '2018-03-18T09:00:00+07:00'
        @apiParam {datetime} end_time format '2018-03-18T09:00:00+07:00'
        ....

        @apiSuccess {object} event
        @apiSuccessExample {json}
        {
            "kind": "calendar#event",
            "creator": {
                "email": "thqbop1@gmail.com"
            },
            "iCalUID": "24m6ps5v1vtardfihidsb1nsig@google.com",
            "reminders": {
                "useDefault": true
            },
            "attachments": [
                {
                    "title": "IMG_2726.JPG",
                    "iconLink": "https://ssl.gstatic.com/docs/doclist/images/icon_10_generic_list.png",
                    "fileId": "1SOkB6uHsdfXmn2oY31D5g0t_0P6Wqzn1",
                    "fileUrl": "https://drive.google.com/file/d/1SOkB6uHsdfXmn2oY31D5g0t_0P6Wqzn1/view?usp=drive_web"
                }
            ],
            "etag": "\"3042179875790000\"",
            "summary": "Abc222",
            "attendees": [
                {
                    "self": true,
                    "displayName": "Hàn Quốc Trương",
                    "responseStatus": "accepted",
                    "email": "thqbop@gmail.com"
                },
                {
                    "organizer": true,
                    "responseStatus": "accepted",
                    "email": "thqbop1@gmail.com"
                }
            ],
            "status": "confirmed",
            "end": {
                "dateTime": "2018-03-12T14:00:00+07:00"
            },
            "updated": "2018-03-15T04:58:57.895Z",
            "sequence": 0,
            "htmlLink": "https://www.google.com/calendar/event?eid=MjRtNnBzNXYxdnRhcmRmaWhpZHNiMW5zaWcgdGhxYm9wQG0",
            "start": {
                "dateTime": "2018-03-12T11:30:00+07:00"
            },
            "created": "2018-03-15T04:16:32.000Z",
            "organizer": {
                "email": "thqbop1@gmail.com"
            },
            "id": "24m6ps5v1vtardfihidsb1nsig"
        }
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            data = request.data.copy()
            timezone = data.get("timezone", "UTC")
            event_id = kwargs.get("pk",None)
            if event_id:
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
                event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
                return Response(event)
            else:
                return Response("Event id is required!", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def delete(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {DELETE} /event/:id delete event
        @apiName EventDelete
        @apiGroup Ribo_api Event
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
           "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiSuccess 200
        """
        try:
            user = self.request.user
            service = OauthService._get_service(user.id)
            event_id = kwargs.get("pk",None)
            if event_id:
                service.events().delete(calendarId='primary',  eventId=event_id).execute()
                return Response("Deleted", status=status.HTTP_200_OK)
            else:
                return Response("Event id is required!", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            Utils.log_exception(e)
            raise e