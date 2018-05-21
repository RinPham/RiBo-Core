import json
import random

import pytz
from django.db import transaction
from django.utils import timezone
import datetime
from ribo_api.const import TaskType, Recurrence, weekday
from ribo_api.models.message import Message, ContentMessage
from ribo_api.models.task import Task
from ribo_api.serializers.message import  MessageSerializer
from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.base import BaseService
from ribo_api.services.dialogflow import ApiAIService
from ribo_api.services.event import EventService
from ribo_api.services.oauth import OauthService
from ribo_api.services.task import TaskService
from ribo_api.services.utils import Utils
from ribo_api.string import MSG_STRING
from dateutil import parser


class ConversationService(BaseService):

    @classmethod
    def load_messages(cls, user_id, **kwargs):
        limit = kwargs.get("limit",20)
        page = kwargs.get("page",0)
        offset = limit*page
        messages = Message.objects(user_id=user_id).order_by("-id")[offset:offset+limit]
        if not messages:
            message = Message()
            message['user_id'] = user_id
            message.content = ContentMessage(question_text='Hello, Can I help you with something?', answer_text='',
                                             from_who=0)
            message['action'] = 'greeting'
            message['next_question_id'] = None
            message.save()
            messages = Message.objects(user_id=user_id).order_by("-id")[offset:offset + limit]
        return MessageSerializer(messages, many=True).data

    @classmethod
    def reply(cls, data, **kwargs):
        user_id = data.get("user_id",0)
        body = data.get("body","")
        tz = pytz.timezone(data.get('tz', 'Asia/Bangkok'))
        object_id = data.get("object_id", None)
        messages = []
        if body:
            with transaction.atomic():
                try:
                    message = Message.objects(user_id=user_id).order_by("-id")[0]
                    if message['content']['answer_text']:
                        message = Message()
                        message['user_id'] = user_id
                        message.content = ContentMessage(question_text=body, answer_text='', from_who=1)
                        message['action'] = None
                        message['next_question_id'] = None
                        message.save()
                    else:
                        message = cls.save_user_message(body, user_id)
                    result = cls.process_reply(user_id,body, message, object_id=object_id, tz=tz)
                    response = result['response']
                    res_message = cls.create_message(response, user_id, result, 0)
                    if result.get('finish',False):
                        text = MSG_STRING.NEED_RIBO[random.randint(0, len(MSG_STRING.NEED_RIBO)-1)]
                        res_message2 = cls.create_message(text, user_id, result, 0)
                        messages.append(res_message2)
                    messages.append(res_message)
                    return reversed(messages)
                except Exception as e:
                    Utils.log_exception(e)
                    message = cls.create_message(e.args[0], user_id, {}, 0)
                    messages.append(message)
                    return messages


    @classmethod
    def save_user_message(cls, body, user_id, **kwargs):
        message = Message.objects(user_id=user_id).order_by("-id")[0]
        message['content']['answer_text'] = body
        message['updated_at'] = timezone.now()
        message.save()
        return message

    @classmethod
    def create_message(cls, text, user_id, data, next_question, **kwargs):
        message = Message()
        message['user_id'] = user_id
        message.content = ContentMessage(question_text=text, answer_text='', from_who=0)
        message['action'] = data.get('action','')
        message['slots'] = data.get('list_slots',[])
        message['next_question_id'] = None
        if next_question:
            message.next_question_id = next_question.id
        message.save()
        return message


    @classmethod
    def process_reply(cls,user_id, text, message, tz, **kwargs):
        ai_result = ApiAIService.get_result(user_id,text)
        params = ai_result['parameters']
        action = ai_result['action']
        fulfillment = ai_result['fulfillment']
        response = fulfillment.get('speech','')
        intent_info = ai_result['metadata']
        if 'cancel' in text.lower():
            ApiAIService.del_contents(user_id)
            action = 'confirmation.no'
        result = None
        finish = False
        data = {}
        if 'reminder' in action:
            if action == 'reminders.add':
                task_data = {
                    'user_id': user_id,
                    'location': params.get('location', '')
                }
                date_time = params.get('date-time', [])
                name = params.get('name', '')
                recurrences = params.get('recurrence', [])
                task_data['at_time'] = []
                if date_time:
                    if '/' in date_time[0]:
                        date_time = date_time.split('/')
                    if recurrences and (recurrences[0] in Recurrence.RECURRENCE_WEEKLY) and ('weekly' not in recurrences):
                        date_time = cls.get_datetime(params)
                    for date in date_time:
                        date = Utils.parse_datetime(date, tz)
                        task_data['at_time'].append(date)
                if name:
                    task_data['title'] = name
                    if 'call' in name.lower():
                        task_data['type'] = TaskType.CALL
                    elif 'email' in name.lower():
                        task_data['type'] = TaskType.EMAIL
                if name and date_time and recurrences:
                    list_slots = []
                    task_data['recurrence'] = recurrences
                    result = TaskService.create_task(data=task_data)
                    response = "I've just added your reminder: "
                    for item in result:
                        response += "\n" + TaskService.render_reminder_str(item, tz)
                        list_slots.append(json.dumps(dict(item)))
                    data.update({'list_slots': list_slots})
            elif action == 'reminders.get':
                query_data = cls.prepare_query(user_id,params,tz)
                results = TaskService.get_task(query_data, exclude_done=False, tz=tz)
                if results:
                    response = 'Your reminders: '
                    list_slots = []
                    for i,item in enumerate(results):
                        list_slots.append(json.dumps(dict(item)))
                        if i < 3:
                            response += "\n {0}. ".format(str(i+1)) + TaskService.render_reminder_str(item, tz)
                    data.update({'list_slots':list_slots})
                else:
                    response = MSG_STRING.NO_REMINDER
            elif action == 'reminders.remove':
                list_slots = []
                all = params.get('all', False)
                task_id = False
                if intent_info['intentName'] == 'reminders.add - remove':
                    task_item = json.loads(message.slots[0])
                    task_id = task_item.get('id','')
                if kwargs.get('object_id', None) and not all:
                    task = Task.objects(id=kwargs.get('object_id'), user_id=user_id)[0]
                    list_slots.append(json.dumps(dict(TaskSerializer(task).data)))
                    at_time = Utils.utc_to_local(task.at_time, tz).strftime('%b %d, %Y at %I:%M %p')
                    response = MSG_STRING.REMOVE_REMINDER_CONFIRM.format(task.title, at_time)
                elif task_id:
                    task = Task.objects(id=task_id)[0]
                    list_slots.append(json.dumps(dict(TaskSerializer(task).data)))
                    at_time = Utils.utc_to_local(task.at_time, tz).strftime('%b %d, %Y at %I:%M %p')
                    response = MSG_STRING.REMOVE_REMINDER_CONFIRM.format(task.title, at_time)
                else:
                    query_data = cls.prepare_query(user_id, params,tz)
                    results = TaskService.get_task(query_data, exclude_done=True, tz=tz)
                    if results:
                        for item in results:
                            list_slots.append(json.dumps(dict(item)))
                        if all and not (params.get('date-time', '') or params.get('name', '')):
                            response = MSG_STRING.REMOVE_ALL_REMINDER_CONFIRM
                        else:
                            if len(results) == 1:
                                list_slots = [json.dumps(dict(results[0]))]
                                at_time = Utils.utc_to_local_str(results[0]['at_time'], tz)
                                response = MSG_STRING.REMOVE_REMINDER_CONFIRM.format(results[0]['title'], at_time)
                            else:
                                response = "Which reminder do you want to remove?"
                                for i, item in enumerate(results):
                                    if i < 3:
                                        response += "\n {0}. ".format(str(i+1)) + TaskService.render_reminder_str(item, tz)
                                    else:
                                        break
                    else:
                        response = MSG_STRING.NO_REMINDER_REMOVE
                data.update({'list_slots': list_slots})
            elif action == 'reminders.rename':
                list_slots = []
                old_name = params.get('old-name', '')
                new_name = params.get('name', '')
                if kwargs.get('object_id', None):
                    if old_name:
                        task = Task.objects(id=kwargs.get('object_id'))[0]
                        cur_name = task.title
                        task.title = old_name
                        task.save()
                        list_slots.append(json.dumps(dict(TaskSerializer(task).data)))
                        response = 'I renamed reminder about {0} to {1}'.format(cur_name, old_name)
                        ApiAIService.del_contents(user_id)
                    else:
                        response = "What's the new name?"
                else:
                    if old_name and new_name:
                        task = Task.objects(title__icontains=old_name, user_id=user_id)
                        if task:
                            task = task[0]
                            task.title = new_name
                            task.save()
                            list_slots.append(json.dumps(dict(TaskSerializer(task).data)))
                            response = 'I renamed reminder about {0} to {1}'.format(old_name,new_name)
                        else:
                            response = "I didn't found the reminder."
                data.update({'list_slots': list_slots})
        elif 'events' in action:
            if action == 'events.add':
                list_slots = []
                event_data = {
                    'user_id': user_id,
                    'location': params.get('location', ''),
                }
                date_time_1 = params.get('date-time-1', None)
                date_time_2 = params.get('date-time-2', None)
                name = params.get('name', '')
                if date_time_1 and date_time_2:
                    event_data['start_time'], event_data['end_time'] = Utils.parse_start_end_time(date_time_1,date_time_2, tz)
                if name:
                    event_data['summary'] = name
                if date_time_1 and date_time_2 and name:
                    event = EventService.create_event(event_data)
                    response = "I've just scheduled your event: " + EventService.render_event_str(event, tz)
                    list_slots.append(json.dumps(event))
                data.update({'list_slots': list_slots})
            elif action == 'events.get':
                list_slots = []
                items = cls.get_events(params=params, user_id=user_id, tz=tz)
                for item in items:
                    list_slots.append(json.dumps(item))
                if len(items) != 0:
                    response = 'I found {} events:'.format(len(items))
                    for i,item in enumerate(items):
                        if i < 3:
                            response += "\n {0}. ".format(str(i+1)) + EventService.render_event_str(item, tz)
                        else:
                            break
                else:
                    response = "I didn't found the events."
                data.update({'list_slots': list_slots})
            elif action == 'events.remove':
                list_slots = []
                all = params.get('all', False)
                event_id = False
                if intent_info['intentName'] == 'events.add - remove':
                    event_item = json.loads(message.slots[0])
                    event_id = event_item.get('id','')
                service = OauthService._get_service(user_id)
                if kwargs.get('object_id', None) and not all:
                    event = service.events().get(calendarId='primary', eventId=kwargs.get('object_id', None)).execute()
                    list_slots.append(json.dumps(event))
                    response = MSG_STRING.REMOVE_EVENTS_CONFIRM.format(EventService.render_event_str(event, tz))
                elif event_id:
                    event = service.events().get(calendarId='primary', eventId=event_id).execute()
                    if event:
                        list_slots.append(json.dumps(event))
                        response = MSG_STRING.REMOVE_EVENTS_CONFIRM.format(EventService.render_event_str(event, tz))
                    else:
                        response = 'This event was removed!'
                else:
                    results = cls.get_events(params, user_id, tz)
                    if results:
                        for item in results:
                            list_slots.append(json.dumps(item))
                        if all and not (params.get('date-time', '') or params.get('name', '')):
                            response = MSG_STRING.REMOVE_ALL_EVENTS_CONFIRM
                        else:
                            if len(results) == 1:
                                list_slots = [json.dumps(results[0])]
                                response = MSG_STRING.REMOVE_EVENTS_CONFIRM.format(EventService.render_event_str(results[0], tz))
                            else:
                                response = "Which event do you want to remove?"
                                for i, item in enumerate(results):
                                    if i < 3:
                                        response += "\n {0}. ".format(str(i+1)) + EventService.render_event_str(item, tz)
                                    else:
                                        break
                    else:
                        response = MSG_STRING.NO_EVENTS_REMOVE
                data.update({'list_slots': list_slots})
            elif action == 'events.rename':
                list_slots = []
                old_name = params.get('old-name', '')
                new_name = params.get('name', '')
                service = OauthService._get_service(user_id)
                if kwargs.get('object_id', None):
                    if old_name:
                        event = {
                            'summary': old_name,
                            'start': {
                                'dateTime': None
                            },
                            'end': {
                                'dateTime': None
                            }
                        }
                        event = service.events().update(calendarId='primary',
                                                     eventId=kwargs.get('object_id', None), body=event).execute()
                        list_slots.append(json.dumps(event))
                        response = 'I renamed event about {0} to {1}'.format(event.get('summary', '(No title)'), old_name)
                        ApiAIService.del_contents(user_id)
                    else:
                        response = "What's the new name?"
                else:
                    if old_name and new_name:
                        events = cls.get_events(params={'name':old_name}, user_id=user_id, tz=tz)
                        if events:
                            for event in events:
                                event_id = event.get('id', None)
                                event_data = {
                                    'summary': new_name,
                                    'start': {
                                        'dateTime': event['start']['dateTime']
                                    },
                                    'end': {
                                        'dateTime': event['end']['dateTime']
                                    }
                                }
                                event = service.events().update(calendarId='primary',
                                                                eventId=event_id,
                                                                body=event_data).execute()
                                list_slots.append(json.dumps(event))
                            response = 'I renamed events about {0} to {1}'.format(old_name, new_name)
                        else:
                            response = "I didn't found the event."
                data.update({'list_slots': list_slots})
        elif action == 'confirmation.yes':
            response = cls.process_confirm_yes(message)
        elif action == 'confirmation.no':
            response = 'OK'
            ApiAIService.del_contents(user_id)
        data.update({
            'action': action,
            'response' : response,
            'finish': finish,
            'result': result
        })
        return data


    @classmethod
    def get_datetime(cls,data):
        recurrences = data.get('recurrence', [])
        list_times = data.get('date-time', [])
        list_date_time = []
        result = []
        for _recur in recurrences:
            if _recur in Recurrence.RECURRENCE_WEEKLY:
                date_number = weekday[_recur]
                list_date_time.append(Utils.next_weekday(date_number).strftime('%Y-%m-%d'))
            elif _recur == Recurrence.RECURRENCE_WEEKENDS:
                list_date_time.append(Utils.next_weekday(5).strftime('%Y-%m-%d'))
            elif _recur == Recurrence.RECURRENCE_WEEKDAYS:
                list_date_time.append(Utils.next_weekday(0).strftime('%Y-%m-%d'))
        for time in list_times:
            for date in list_date_time:
                result.append(date +'T'+ parser.parse(time).time().strftime('%H:%M:%S') + 'Z')
        return result

    @classmethod
    def prepare_query_date(cls,date, start=False):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            try:
                datetime.datetime.strptime(date, '%H:%M:%S')
                date = datetime.datetime.today().strftime('%Y-%m-%d') + 'T' + date + 'Z'
            except ValueError:
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                    if start:
                        date = date + 'T00:00:00Z'
                    else:
                        date = date + 'T23:59:59Z'
                except ValueError as e:
                    raise e
        return date

    @classmethod
    def prepare_query(cls, user_id, params, tz):
        query_data = {'user_id': user_id}
        date = params.get('date-time', '')
        name = params.get('name', '')
        time_period = params.get('time-period','')
        if '/' in date:
            query_data['at_time__gte'] = Utils.parse_datetime(cls.prepare_query_date(date.split('/')[0], start=True),
                                                              tz).strftime('%Y-%m-%dT%H:%M:%SZ')
            query_data['at_time__lte'] = Utils.parse_datetime(cls.prepare_query_date(date.split('/')[1], start=False),
                                                              tz).strftime('%Y-%m-%dT%H:%M:%SZ')
        elif date:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                query_data['at_time__gte'] = Utils.parse_datetime(cls.prepare_query_date(date, start=True),
                                                                  tz).strftime('%Y-%m-%dT%H:%M:%SZ')
                query_data['at_time__lte'] = Utils.parse_datetime(cls.prepare_query_date(date, start=False),
                                                                  tz).strftime('%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                query_data['at_time'] = Utils.parse_datetime(cls.prepare_query_date(date), tz).strftime(
                    '%Y-%m-%dT%H:%M:%SZ')
        if name:
            query_data['title__contains'] = name
        return query_data

    @classmethod
    def process_confirm_yes(cls, message):
        response = ''
        if message.action == 'reminders.remove':
            for item in message.slots:
                try:
                    data = json.loads(item)
                    task = Task.objects(id=data['id'])[0]
                    task.delete()
                except Exception:
                    pass
            response = 'I removed it'
        elif message.action == 'events.remove':
            service = OauthService._get_service(message.user_id)
            for item in message.slots:
                try:
                    data = json.loads(item)
                    service.events().delete(calendarId='primary', eventId=data['id']).execute()
                except Exception:
                    pass
            response = 'I removed it'
        return response

    @classmethod
    def get_events(cls, params, user_id, tz):
        service = OauthService._get_service(user_id)
        timeMax = ''
        timeMin = ''
        date_time = params.get('date-time', [])
        name = params.get('name', '').lower()
        location = params.get('location', '').lower()
        if date_time:
            if len(date_time) == 1:
                if '/' in date_time[0]:
                    timeMax = Utils.parse_datetime(cls.prepare_query_date(date_time[0].split('/')[1], start=False),
                                                   tz, True)
                    timeMin = Utils.parse_datetime(cls.prepare_query_date(date_time[0].split('/')[0], start=True),
                                                   tz, True)
                else:
                    timeMax = (Utils.parse_datetime(cls.prepare_query_date(date_time[0], start=False),
                                                    tz, True) + datetime.timedelta(minutes=1))
                    timeMin = Utils.parse_datetime(cls.prepare_query_date(date_time[0], start=True),
                                                   tz, True)
            elif len(date_time) == 2:
                timeMax = Utils.parse_datetime(cls.prepare_query_date(date_time[0], start=False),
                                                tz, True)
                timeMin = Utils.parse_datetime(cls.prepare_query_date(date_time[1], start=True),
                                               tz, True)

            if timeMax < timeMin:
                timeMax, timeMin = timeMin, timeMax
            timeMax = timeMax.strftime('%Y-%m-%dT%H:%M:%S%z')
            timeMin = timeMin.strftime('%Y-%m-%dT%H:%M:%S%z')
        query_text = ''
        if name:
            query_text = name
        if location:
            query_text = location + " + " + query_text
        if date_time:
            result = service.events().list(calendarId='primary', timeMax=timeMax, timeMin=timeMin,
                                           q=query_text).execute()
        else:
            result = service.events().list(calendarId='primary', q=query_text).execute()
        items = result.get('items', [])
        _temp_items = [item for item in items]
        if (name or location) and _temp_items:
            for item in _temp_items:
                is_remove = False
                if name and (name not in item['summary'].lower()):
                    items.remove(item)
                    is_remove = True
                if not is_remove and location and (location not in item['location'].lower()):
                    items.remove(item)
        return items
