from ribo_api.const import TypeRepeat, Recurrence
from ribo_api.models.task import Task
from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.base import BaseService


class TaskService(BaseService):

    @classmethod
    def create_task(cls, data, **kwargs):
        recurrences = data.get('recurrence', '')
        data['repeat'] = TypeRepeat.NONE
        if recurrences[0] in Recurrence.RECURRENCE_WEEKLY:
            data['repeat'] = TypeRepeat.WEEKLY
        elif recurrences[0] == Recurrence.RECURRENCE_DAILY:
            data['repeat'] = TypeRepeat.DAILY
        elif recurrences[0] == Recurrence.RECURRENCE_MONTHLY:
            data['repeat'] = TypeRepeat.MONTHLY
        elif recurrences[0] == Recurrence.RECURRENCE_WEEKDAYS:
            data['repeat'] = TypeRepeat.WEEKDAYS
        elif recurrences[0] == Recurrence.RECURRENCE_WEEKENDS:
            data['repeat'] = TypeRepeat.WEEKENDS
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @classmethod
    def get_task(cls,data, **kwargs):
        if data.get('at_time','') and data.get('title',''):
            items = Task.object(title__contains=data.get('title',''), at_time=data.get('at_time',''))
        elif data.get('at_time',''):
            items = Task.object(at_time=data.get('at_time', ''))
        elif data.get('title',''):
            items = Task.object(title__contains=data.get('title', ''))
        return TaskSerializer(data=items, many=True).data

