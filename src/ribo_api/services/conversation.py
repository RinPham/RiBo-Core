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
from ribo_api.services.task import TaskService
from ribo_api.services.utils import Utils
from ribo_api.string import MSG_STRING
from dateutil import parser

from ribo_core.utilstz import get_local_time


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
                    result = cls.process_reply(user_id,body, message,tz=tz)
                    response = result['response']
                    res_message = cls.create_message(response, user_id, result, 0)
                    if result.get('finish',False):
                        text = MSG_STRING.NEED_RIBO[random.randint(0, len(MSG_STRING.NEED_RIBO)-1)]
                        res_message2 = cls.create_message(text, user_id, result, 0)
                        messages.append(res_message2)
                    messages.append(res_message)
                    return reversed(messages)
                except Exception as e:
                    raise e


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
                    task_data['recurrence'] = recurrences
                    result = TaskService.create_task(data=task_data)
                    message['slots'] = [result]
                    finish = True
            elif action == 'reminders.get':
                query_data = cls.prepare_query(user_id,params,tz)
                results = TaskService.get_task(query_data, exclude_done=False, tz=tz)
                if results:
                    response = 'Your reminders: '
                    list_slots = []
                    for i,item in enumerate(results):
                        list_slots.append(json.dumps(dict(item)))
                        if i <= 3:
                            response += TaskService.render_reminder_str(i, item, tz)
                    data.update({'list_slots':list_slots})
                else:
                    response = MSG_STRING.NO_REMINDER
            elif action == 'reminders.reschedule':
                pass
            elif action == 'reminders.remove':
                list_slots = []
                all = params.get('all', False)
                if kwargs.get('task_id', None) and not all:
                    task = Task.objects(id=kwargs.get('task_id'), user_id=user_id)
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
                                    response += TaskService.render_reminder_str(i, item, tz)
                    else:
                        response = MSG_STRING.NO_REMINDER_REMOVE
                data.update({'list_slots': list_slots})
            elif action == 'reminders.rename':
                pass
        elif 'event' in action:
            pass
        elif action == 'smalltalk.confirmation.yes':
            response = cls.process_confirm_yes(message)
        elif action == 'smalltalk.confirmation.no':
            response = 'OK'
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
                list_date_time.append(Utils.next_weekday(date_number))
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
                    task = Task.objects(id=data['id'])
                    task.delete()
                except Exception:
                    pass
            response = 'I removed it'
        return response


