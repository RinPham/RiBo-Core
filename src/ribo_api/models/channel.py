from mongoengine import Document, fields

class Channel(Document):
    user_id = fields.StringField(required=True,unique=True)

    class Meta:
        app_label = 'no_sql'

    def __unicode__(self):
        return self.user_id