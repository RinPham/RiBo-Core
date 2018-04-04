from mongoengine import fields
from mongoengine.document import EmbeddedDocument

from ribo_api.models.timestamped import TimeStampedModel


class ContentMessage(EmbeddedDocument):
    answer_text = fields.StringField(null=True)
    question_text = fields.StringField(null=True)
    from_who = fields.IntField() # 0: ribo assistant, 1: user



class Message(TimeStampedModel):
    user_id = fields.ObjectIdField(required=True)
    content = fields.EmbeddedDocumentField(ContentMessage, required=True)
    action = fields.StringField(null=True)
    next_question_id = fields.ObjectIdField(default=None, null=True)


    class Meta:
        app_label = 'nosql'
