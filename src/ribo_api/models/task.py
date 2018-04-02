from mongoengine import Document,fields

class Task(Document):
    title = fields.StringField(required=True)
    user_id = fields.ObjectIdField(required=True)
    at_time = fields.DateTimeField(required=False)
    done = fields.BooleanField(default=False)
    repeat = fields.IntField(default=False) # 0: None, 1: Daily, 2: Weekly, 3: Weekdays

    class Meta():
        app_label = 'no_sql'
