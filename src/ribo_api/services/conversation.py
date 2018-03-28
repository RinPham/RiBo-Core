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
                    else:
                        is_question = False
                        next_question = None
                        if is_question:
                            next_question = message['content']['question_text']
                        message = cls.save_message(body, user_id, is_question, data)
                    aibot_response = ApiAIService.get_response(body)
                    print(aibot_response)
                except:
                    pass


    @classmethod
    def save_message(cls, body, user_id, is_question=False, next_question=None, **kwargs):
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
