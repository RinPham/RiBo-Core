from mongoengine import Document,fields

class User(Document):
    email = fields.EmailField(required=True, unique=True)
    first_name = fields.StringField()
    last_name = fields.StringField()
    birthday = fields.StringField()
    sex = fields.IntField()
    avatar = fields.StringField()

    class Meta():
        app_label = 'no_sql'

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True
