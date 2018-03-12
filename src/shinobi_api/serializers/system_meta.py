#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Feb 17 2017, 11:19 AM$"

from shinobi_api.serializers import ServiceSerializer
from shinobi_api.services.msystem import MSystemService
from shinobi_api.models import SystemMeta


class SystemMetaSerializer(ServiceSerializer):
    def create(self, validated_data):
        try:
            return MSystemService.save(validated_data)
        except TypeError as e:
            raise e

    def update(self, instance, validated_data):
        try:
            validated_data['id'] = instance.id
            return MSystemService.save(validated_data)
        except TypeError as e:
            raise e

    class Meta:
        model = SystemMeta
