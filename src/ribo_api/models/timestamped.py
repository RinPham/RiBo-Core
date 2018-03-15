from mongoengine import Document, fields
from django.utils import timezone

class TimeStampedModel(Document):
    created_at = fields.DateTimeField(default=timezone.now)
    updated_at = fields.DateTimeField(default=timezone.now)

    meta = {'abstract': True}

    class Meta:
        app_label = 'no_sql'