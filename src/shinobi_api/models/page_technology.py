from mongoengine import Document,EmbeddedDocument,fields
from shinobi_api.models.element import Element

class PageTechnology(Document):
    id_page = fields.StringField(required=True)
    os = fields.StringField(required=True)
    browser = fields.StringField(required=True)

    class Meta:
        app_label = 'no_sql'
