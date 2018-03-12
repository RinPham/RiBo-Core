#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hieunh"
__date__ = "$Jul 21 2016, 03:05 PM$"

from shinobi_api.serializers import ServiceSerializer, serializers
from shinobi_api.models.location import Location


class LocationSerializer(ServiceSerializer):
    city = serializers.CharField(required=False)

    class Meta:
        model = Location
