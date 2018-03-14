from mongoengine import Document,fields

class User(Document):
    email = fields.EmailField(required=True, unique=True)
    full_name = fields.StringField()
    birthday = fields.StringField()
    sex = fields.IntField()

    class Meta():
        app_label = 'no_sql'
