from mongoengine import fields

from ribo_api.models.timestamped import TimeStampedModel


class Event(TimeStampedModel):
    event_id = fields.StringField()
    user_id = fields.ObjectIdField()
