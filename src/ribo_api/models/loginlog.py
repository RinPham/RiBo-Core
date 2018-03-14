from django.db import models
from django.conf import settings
from django.utils import timezone


class LoginLog(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    api_id = models.PositiveIntegerField(default=0)
    user_agent = models.CharField(max_length=256)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(default=timezone.now)
    device_id = models.CharField(max_length=256, default='')
    time_since_last_login = models.PositiveIntegerField(default=0)
    time_since_last_open_app = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'ribo_logins'