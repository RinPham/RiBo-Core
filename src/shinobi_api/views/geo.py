#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "07 26 2016, 2:20 PM"

from rest_framework.decorators import list_route
from rest_framework.response import Response

from shinobi_api.serializers.location import LocationSerializer
from shinobi_api.models import Location
from shinobi_api.decorators import logging
from shinobi_api.views import BaseViewSet


class GeoViewSet(BaseViewSet):
    view_set = 'geo'
    permission_classes = ()

    @list_route(methods=['get'])
    @logging.ignore
    def locations(self, request, *args, **kwargs):
        """
        """
        country = request.query_params.get('country', 'US')
        locations = Location.objects.order_by("admin1_name").filter(country=country)
        serializer = LocationSerializer(instance=locations, many=True)
        return Response(serializer.data)
