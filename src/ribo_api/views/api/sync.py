from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.db import transaction
from ribo_api.models.task import Task
from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.oauth import OauthService
from ribo_api.services.utils import Utils


class SyncViewSet(ViewSet):
    view_set = 'sync'
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /sync sync create
        @apiName sync
        @apiGroup Ribo_api Sync
        @apiPermission Authentication

        @apiHeader {string} Authorization format: token <token_string>
        @apiHeaderExample {json} Request Header Example:
        {
            "Authorization": "token QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J"
        }

        @apiParamExample {json} Params Example
        {
            "create":{
                "reminders":[
                    {
                        "title": "quoc test 4",
                        "at_time": "2018-09-08T07:00:00+0700",
                        "repeat": 0
                    },
                    {
                        "title": "quoc test 5",
                        "at_time": "2018-09-08T09:00:00+0700",
                        "repeat": 0
                    }
                ],
                "events":[
                    {
                        "summary": "quoc 3",
                        "description": "",
                        "location":"",
                        "start_time": "2018-05-29T09:00:00+07:00",
                        "end_time": "2018-05-29T10:00:00+07:00"
                    },
                    {
                        "summary": "quoc 4",
                        "description": "",
                        "location":"",
                        "start_time": "2018-05-29T08:00:00+07:00",
                        "end_time": "2018-05-29T09:00:00+07:00"
                    }
                ]
            },
            "update":{
                "reminders":[
                    {
                        "id": "5b0b755b012a0f2f462d93d3",
                        "title": "quoc test 4",
                        "at_time": "2018-09-08T07:00:00+0700",
                        "repeat": 0
                    },
                    {
                        "id": "5b0b755b012a0f2f462d93d4",
                        "title": "quoc test 5",
                        "at_time": "2018-09-08T09:00:00+0700",
                        "repeat": 0
                    }
                ],
                "events":[
                    {
                        "id": "7tunq4gk2lknu20alui72du178",
                        "summary": "quoc 3",
                        "description": "",
                        "location":"",
                        "start_time": "2018-05-29T09:00:00+07:00",
                        "end_time": "2018-05-29T10:00:00+07:00"
                    },
                    {
                        "id": "6qefhv5nl039gdm06fvkg0rmts",
                        "summary": "quoc 4",
                        "description": "",
                        "location":"",
                        "start_time": "2018-05-29T08:00:00+07:00",
                        "end_time": "2018-05-29T09:00:00+07:00"
                    }
                ]
            },
            "delete:{
                "reminders":[
                    {
                        "id": "5b0b755b012a0f2f462d93d3",
                        "title": "quoc test 4",
                        "at_time": "2018-09-08T07:00:00+0700",
                        "repeat": 0
                    },
                    {
                        "id": "5b0b755b012a0f2f462d93d4",
                        "title": "quoc test 5",
                        "at_time": "2018-09-08T09:00:00+0700",
                        "repeat": 0
                    }
                ],
                "events":[
                    {
                        "id": "7tunq4gk2lknu20alui72du178",
                        "summary": "quoc 3",
                        "description": "",
                        "location":"",
                        "start_time": "2018-05-29T09:00:00+07:00",
                        "end_time": "2018-05-29T10:00:00+07:00"
                    },
                    {
                        "id": "6qefhv5nl039gdm06fvkg0rmts",
                        "summary": "quoc 4",
                        "description": "",
                        "location":"",
                        "start_time": "2018-05-29T08:00:00+07:00",
                        "end_time": "2018-05-29T09:00:00+07:00"
                    }
                ]
            }
        }

        @apiSuccess {object} event
        @apiSuccessExample {json}
        {
            "success": true,
        }
        """
        with transaction.atomic():
            try:
                user = self.request.user
                data = request.data.copy()
                create = data.get("create", {})
                update = data.get("update", {})
                delete = data.get("delete", {})
                service = OauthService._get_service(user.id)
                if create:
                    reminders = create.get('reminders', [])
                    events = create.get('events',[])
                    timezone = create.get("timezone", "UTC")
                    for reminder_item in reminders:
                        reminder_item['user_id'] = user.id
                        serializer = self.serializer_class(data=reminder_item)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                    for event_item in events:
                        event = {
                            'summary': event_item.get('summary',None),
                            'location': event_item.get('location',None),
                            'description': event_item.get('description',None),
                            'start': {
                                'dateTime': event_item.get('start_time',None),
                                'timeZone': timezone,
                            },
                            'end': {
                                'dateTime': event_item.get('end_time',None),
                                'timeZone': timezone,
                            },
                            'reminders': {
                                'useDefault': False,
                            },
                        }
                        event = service.events().insert(calendarId='primary', body=event).execute()
                    if update:
                        reminders = update.get('reminders', [])
                        events = update.get('events', [])
                        timezone = update.get("timezone", "UTC")
                        for reminder_item in reminders:
                            task = Task.objects(id=reminder_item.get('id', 0))
                            if task:
                                task = task[0]
                                serializer = self.serializer_class(task, data=reminder_item, partial=True)
                                serializer.is_valid(raise_exception=True)
                                serializer.save()
                        for event_item in events:
                            event = {
                                'summary': event_item.get('summary', None),
                                'location': event_item.get('location', None),
                                'description': event_item.get('description', None),
                                'start': {
                                    'dateTime': event_item.get('start_time', None),
                                    'timeZone': timezone,
                                },
                                'end': {
                                    'dateTime': event_item.get('end_time', None),
                                    'timeZone': timezone,
                                },
                                'reminders': {
                                    'useDefault': False,
                                },
                            }
                            event = service.events().update(calendarId='primary', eventId=event_item.get("id", 0),
                                                            body=event).execute()
                    if delete:
                        reminders = delete.get('reminders', [])
                        events = delete.get('events', [])
                        for reminder_item in reminders:
                            task = Task.objects(id=reminder_item.get('id', 0))
                            if task:
                                task.delete()
                        for event_item in events:
                            service.events().delete(calendarId='primary',  eventId=event_item.get('id',0)).execute()
                return Response({'success':True})
            except Exception as e:
                Utils.log_exception(e)
                raise e
