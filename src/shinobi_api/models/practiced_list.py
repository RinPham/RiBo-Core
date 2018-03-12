from mongoengine import Document,fields

class PracticedList(Document):
    type = fields.StringField()
    labels = fields.ListField()
    practiced_list = fields.ListField()

    class Meta:
        app_label = 'no_sql'