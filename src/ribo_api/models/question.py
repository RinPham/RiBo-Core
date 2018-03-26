from mongoengine import Document, fields


class Question(Document):
    content = fields.StringField()

    class Meta:
        app_label = 'nosql'
