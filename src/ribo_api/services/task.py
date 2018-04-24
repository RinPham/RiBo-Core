from datetime import datetime

from mongoengine.queryset.visitor import Q

from ribo_api.const import TypeRepeat, Recurrence
from ribo_api.models.task import Task
from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.base import BaseService


class TaskService(BaseService):

    @classmethod
    def create_task(cls, data, **kwargs):
        at_times = data.get("at_time", [])
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
        for at_time in at_times:
            data['at_time'] = at_time
            serializer = TaskSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return serializer.data

    @classmethod
    def get_task(cls,data, **kwargs):
        query = cls.prepare_filter(data)
        items = Task.objects(query)
        task_serializer = TaskSerializer(items, many=True)
        return task_serializer.data

    @classmethod
    def prepare_filter(cls,data):
        q = Q(user_id=data.get('user_id', ''))
        if data.get('at_time__gte',''):
            q = q & Q(at_time__gte=data.get('at_time__gte','')) & Q(at_time__lte=data.get('at_time__lte',''))
        elif data.get('at_time',''):
            q = q & Q(at_time=datetime.strptime(data.get('at_time',''), '%Y-%m-%d'))
        if data.get('title__contains',''):
            q = q & Q(title__contains=data.get('title__contains', ''))
        return q