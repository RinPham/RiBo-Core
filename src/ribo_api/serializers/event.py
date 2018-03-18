from rest_framework_mongoengine.serializers import DocumentSerializer

from ribo_api.models.events import Event
from ribo_api.models.task import Task


class EventSerializer(DocumentSerializer):
    class Meta:
        model = Event
        fields = '__all__'