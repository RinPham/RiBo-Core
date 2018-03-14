from rest_framework_mongoengine.serializers import DocumentSerializer

from ribo_api.models.task import Task


class TaskSerializer(DocumentSerializer):
    class Meta:
        model = Task
        fields = '__all__'