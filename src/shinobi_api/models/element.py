from mongoengine import EmbeddedDocument,fields
from shinobi_api.models.event import Event

class Element(EmbeddedDocument):
    dataType = fields.StringField(required=False, null=True)
    elementName = fields.StringField(required=False, null=True)
    id = fields.StringField(required=False, null=True)
    labels = fields.StringField(required=False, null=True)
    classElement =  fields.StringField(required=False, null=True)
    value = fields.ListField(fields.StringField(null=True),required=False,null=True)
    event = fields.ListField(fields.EmbeddedDocumentField(Event),required=False,null=True)
    htmlString = fields.StringField(required=True)
    coordinates = fields.StringField(required=False, null=True)
    shinobiId = fields.StringField(required=True)
    practiceList = fields.ListField(fields.StringField(null=True),required=False,null=True)
    tested = fields.BooleanField(default=False)
    showIssue = fields.BooleanField(required=False, null=True)
    recordNotification = fields.StringField(required=False, null=True)

    class Meta:
        app_label = 'no_sql'