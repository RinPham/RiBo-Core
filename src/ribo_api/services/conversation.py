from django.db import transaction
from django.utils import timezone
from ribo_api.models.message import Message
from ribo_api.serializers.message import ContentMessageSerializer, MessageSerializer
from ribo_api.services.base import BaseService
from ribo_api.services.dialogflow import DialogFlow, ApiAIService


class ConversationService(BaseService):

    @classmethod
    def load_messages(cls, user_id, **kwargs):
        limit = kwargs.get("limit",20)
        page = kwargs.get("page",0)
        offset = limit*page
        messages = Message.objects(user_id=user_id).order_by("-id")[offset:offset+limit]
        return MessageSerializer(messages, many=True).data

    @classmethod
    def reply(cls, data, **kwargs):
        user_id = data.get("user_id",0)
        body = data.get("body","")
        is_question = False
        if body:
            with transaction.atomic():
                try:
                    message = Message.objects(user_id=user_id).order_by("-id")[0]
                    if message['content']['answer_text']:
                        message = Message()
                        message['user_id'] = user_id
                        message['content'] = {
                            'question_text' : body,
                            'answer_text': '',
                            'from_who': 1
                        }
                        message['action'] = None
                        message['next_question_id'] = None
                        message.save()
                    else:
                        is_question = False
                        next_question = None
                        if is_question:
                            pass
                        message = cls.save_message(body, user_id, data, is_question, next_question)
                    result = cls.process_reply(user_id,body)
                    if is_question:
                        answer_result = result['answer']
                        message = cls.save_message(answer_result, user_id, data, False)
                    return message
                except:
                    pass


    @classmethod
    def save_message(cls, body, user_id, data, is_question=False, next_question=None,**kwargs):
        if is_question:
            message = Message()
            message['user_id'] = user_id
            message['content'] = {
                'question_text': body,
                'answer_text': '',
                'from_who': 1
            }
            message['action'] = None
            message['next_question_id'] = None
            if next_question:
                message.next_question_id = next_question.id
        else:
            message = Message.objects(user_id=user_id).order_by("-id")[0]
            message['content']['answer'] = body
            message['updated_at'] = timezone.now()
        message.save()
        return message


    @classmethod
    def process_reply(cls,user_id, text):
        ai_result = ApiAIService.get_result(user_id,text)
        params = ai_result['parameters']
        action = ai_result['action']
        fulfillment = ai_result['fulfillment']
        if 'reminder' in action:
            if action == 'reminders.add':
                task_data = {
                    'title': params['name'],
                    'user_id': user_id,
                    'at_time': params['date-time'],
                    'recurrence': params['recurrence']
                }

        elif 'event' in action:
            pass
        result = {
            'answer' : fulfillment['speech']
        }
        return result
