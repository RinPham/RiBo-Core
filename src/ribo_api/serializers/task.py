from rest_framework_mongoengine.serializers import DocumentSerializer
from ribo_api.models.task import Task


class TaskSerializer(DocumentSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validate_data):
        from ribo_api.services.utils import Utils
        from ribo_api.services.task import TaskService
        try:
            task = TaskService.save(validate_data)
            return task
        except Exception as e:
            Utils.log(e)
            raise e