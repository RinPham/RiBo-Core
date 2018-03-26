from mongoengine import fields
from mongoengine.document import EmbeddedDocument

from ribo_api.models.timestamped import TimeStampedModel


class ContentMessage(EmbeddedDocument):
    answer_text = fields.StringField()
    question_text = fields.StringField()
    from_who = fields.IntField() # 0: ribo assistant, 1: user



class Message(TimeStampedModel):
    user_id = fields.ObjectIdField(required=True)
    content = fields.EmbeddedDocumentField(ContentMessage, required=True)
    action = fields.StringField()
    next_question_id = fields.ObjectIdField()


    class Meta:
        app_label = 'nosql'
