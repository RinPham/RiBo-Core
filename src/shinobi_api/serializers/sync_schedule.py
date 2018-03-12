#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

from shinobi_api.serializers import serializers
from shinobi_api.serializers import ServiceSerializer
from shinobi_api.models.sync_schedule import SyncSchedule

__author__ = "tu"
__date__ = "$April 13 2017, 08:05 AM$"


class SyncScheduleSerializer(ServiceSerializer):

    def create(self, validated_data):
        return SyncSchedule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.save()
        return instance

    class Meta:
        model = SyncSchedule
