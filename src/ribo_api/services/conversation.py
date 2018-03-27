from ribo_api.models.message import Message
from ribo_api.serializers.message import ContentMessageSerializer
from ribo_api.services.base import BaseService


class ConversationService(BaseService):
    pass
    # @classmethod
    # def save_message(cls, user_id, msg_id, data, **kwargs):
    #     contentMsgSerializer = ContentMessageSerializer(data)
    #     data['content'] = contentMsgSerializer.data
    #     try:
    #         msg = Message.objects(pk=msg_id)
    #         msg =
    #     except:
    #         msg = Message()
    #         msg[]
