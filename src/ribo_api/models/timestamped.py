from mongoengine import Document, fields
from django.utils import timezone

class TimeStampedModel(Document):
    created_at = fields.DateTimeField(default=timezone.now)
    updated_at = fields.DateTimeField(default=timezone.now)
    
    class Meta:
        abstract = True
        app_label = 'no_sql'