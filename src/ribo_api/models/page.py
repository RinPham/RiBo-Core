from mongoengine import Document,EmbeddedDocument,fields

class Page(Document):
    url = fields.StringField(required=True)
    dom_origin = fields.StringField(required=True)
    dom_origin_md5 = fields.StringField(required=True)
    dom_reduce_md5 = fields.StringField(required=True)
    leaves_node = fields.IntField(required=True)
    max_depth = fields.IntField(required=True)
    histogram_color = fields.StringField(required=True)
    full_screen = fields.StringField(required=True)
    test_screen = fields.StringField(required=False)
    listElement = fields.ListField(fields.EmbeddedDocumentField(Element), required=False)
    compare_img1 = fields.StringField(required=False, null=True)
    compare_img2 = fields.StringField(required=False, null=True)

    class Meta:
        app_label = 'no_sql'

