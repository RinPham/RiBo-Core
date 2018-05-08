from datetime import datetime

import pytz
from mongoengine.queryset.visitor import Q

from ribo_api.const import TypeRepeat, Recurrence
from ribo_api.models.task import Task
from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.base import BaseService
from ribo_api.services.utils import Utils


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
        query = cls.prepare_filter(data, **kwargs)
        items = list(Task.objects(query).order_by('at_time'))
        _temp_items = [item for item in items]
        tz = kwargs.get('tz', pytz.timezone('Asia/Bangkok'))
        if data.get('at_time__gte', ''):
            at_time__gte = datetime.strptime(data.get('at_time__gte', ''), '%Y-%m-%dT%H:%M:%SZ')
            at_time__lte = datetime.strptime(data.get('at_time__lte', ''), '%Y-%m-%dT%H:%M:%SZ')
        elif data.get('at_time', ''):
            at_time = datetime.strptime(data.get('at_time', ''), '%Y-%m-%dT%H:%M:%SZ')
        for item in _temp_items:
            at_time_item = Utils.utc_to_local(item['at_time'], tz)
            # check time of at_time in time intervals or equal time of search, endless remove
            if data.get('at_time__gte', ''):
                if (at_time__gte.time() >= at_time_item.time()) and (at_time__lte.time() <= at_time_item.time()):
                    items.remove(item)
                    continue
            elif data.get('at_time', ''):
                if at_time.time() != at_time_item.time():
                    items.remove(item)
                    continue
            # check weekday of at_time in time intervals or equal weekday of search, endless remove
            if item['repeat'] == TypeRepeat.WEEKLY or item['repeat'] == TypeRepeat.WEEKDAYS or item['repeat'] == TypeRepeat.WEEKENDS:
                if data.get('at_time__gte', ''):
                    if at_time_item.weekday() not in Utils.in_weekdays(at_time__gte.weekday(), at_time__lte.weekday()):
                        items.remove(item)
                elif data.get('at_time', ''):
                    if at_time.weekday() != at_time_item.weekday():
                        items.remove(item)
            # check day of month of at_time in time intervals or equal day of month of search, endless remove
            elif item['repeat'] == TypeRepeat.MONTHLY:
                if data.get('at_time__gte', ''):
                    # if month of interval of search time > 2 or (day of at_time in interval of search time with same month)
                    if not ((at_time__lte.month - at_time__gte.month >= 2)
                            or ((at_time__gte.day <= at_time_item.day <= at_time__gte.day)
                                and at_time__lte.month - at_time__gte.month < 1)
                            or (((at_time__gte.day <= at_time_item.day) or (at_time_item.day <= at_time__gte.day))
                                and (at_time__lte.month - at_time__gte.month == 1))):
                        items.remove(item)
                elif data.get('at_time', ''):
                    if at_time.day != at_time_item.day:
                        items.remove(item)
        items = TaskSerializer(items, many=True).data
        return items

    @classmethod
    def prepare_filter(cls, data, **kwargs):
        if kwargs.get('exclude_done', False):
            q = Q(user_id=data.get('user_id', ''))
        else:
            q = Q(user_id=data.get('user_id', '')) & Q(done=False)

        if data.get('at_time__gte',''):
            q = q & Q(at_time__gte=data.get('at_time__gte','')) & Q(at_time__lte=data.get('at_time__lte','')) | Q(repeat__ne=TypeRepeat.NONE)
        elif data.get('at_time',''):
            q = q & Q(at_time=data.get('at_time','')) | Q(repeat__ne=TypeRepeat.NONE)
        if data.get('title__contains',''):
            q = q & Q(title__icontains=data.get('title__contains', ''))
        return q