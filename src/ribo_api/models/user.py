from mongoengine import Document,fields

class User(Document):
    email = fields.EmailField(required=True, primary_key=True)
    access_token = fields.StringField(required=True)
    refresh_token = fields.StringField(required=True)
    expire_time = fields.DateTimeField(required=False)
    json = fields.StringField(default=None)

    class Meta():
        app_label = 'no_sql'
