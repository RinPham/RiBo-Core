from mongoengine import Document,fields

class User(Document):
    email = fields.EmailField(required=True, unique=True)
    access_token = fields.StringField(required=True)
    refresh_token = fields.StringField(required=True)
    expire_time = fields.StringField(required=False)
    json = fields.StringField(default=None)
    full_name = fields.StringField()
    birthday = fields.StringField()
    sex = fields.IntField()

    class Meta():
        app_label = 'no_sql'
