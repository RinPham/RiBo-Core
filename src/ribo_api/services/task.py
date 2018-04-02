from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.base import BaseService


class TaskService(BaseService):

    @classmethod
    def create_task(cls, data, **kwargs):
        recurrence = data.get('recurrence', '')
        if recurrence:
            pass
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
