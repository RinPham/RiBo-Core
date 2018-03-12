from mongoengine import EmbeddedDocument,fields

class Event(EmbeddedDocument):
    name = fields.StringField(required=True)
    statusTest = fields.BooleanField(default=False)

    class Meta:
        app_label = 'no_sql'