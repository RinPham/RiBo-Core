from mongoengine import Document,fields

from ribo_api.const import TaskType


class Task(Document):
    title = fields.StringField(required=True)
    user_id = fields.ObjectIdField(required=True)
    at_time = fields.DateTimeField(required=False)
    type = fields.IntField(default=TaskType.NONE)
    done = fields.BooleanField(default=False)
    repeat = fields.IntField(default=False) # 0: None, 1: Daily, 2: Weekly, 3: Weekdays
    repeat_days = fields.ListField(fields.StringField(default=None))
    email = fields.StringField(null=True)
    phone_number = fields.StringField(null=True)

    class Meta():
        app_label = 'no_sql'
