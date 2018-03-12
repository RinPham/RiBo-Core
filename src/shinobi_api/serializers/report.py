#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

import datetime
from rest_framework import exceptions
from shinobi_api.serializers import serializers
# from shinobi_api.serializers.badge import BadgeSerializer

__author__ = "tu"
__date__ = "$Mars 21 2017, 03:05 PM$"


# class ReportSerializer(serializers.Serializer):
#     start_date = serializers.DateField(required=True, write_only=True)
#     end_date = serializers.DateField(required=True, write_only=True)
#     destination = serializers.CharField(required=False, max_length=256)
#     date = serializers.CharField(required=False, max_length=256)
#     type = serializers.CharField(required=False, max_length=256)
#     data = BadgeSerializer(many=True, required=False)
#     count = serializers.IntegerField(required=False)


class ReportInputSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate_start_date(self, value):
        end_date = datetime.datetime.strptime(self.initial_data.get('end_date'), "%Y-%m-%d").date()
        if value > end_date:
            detail = 'Start date can not be greater than end date.'
            raise exceptions.ValidationError(detail=detail, )
