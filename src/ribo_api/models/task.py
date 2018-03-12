from mongoengine import Document,fields

class Task(Document):
    title = fields.StringField(required=True)
    content = fields.StringField(required=True)
    user_id = fields.ObjectIdField(required=True)
    intent_id = fields.ObjectIdField(required=True)
    at_time = fields.DateTimeField(required=True)
    done = fields.BooleanField(default=False)

    class Meta():
        app_label = 'no_sql'