#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

from shinobi_api.serializers import serializers
from shinobi_api.models.department import Department
from shinobi_api.serializers import ServiceSerializer

__author__ = "tu"
__date__ = "$Mars 21 2017, 03:05 PM$"


class DepartmentSerializer(ServiceSerializer):
    name = serializers.CharField(required=True, allow_blank=True, max_length=14)

    def create(self, validated_data):
        return Department.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', '')
        instance.save()
        return instance

    class Meta:
        model = Department
        fields = (
            'id', 'user', 'name'
        )
        extra_kwargs = {
            'user': {'write_only': True},
        }
