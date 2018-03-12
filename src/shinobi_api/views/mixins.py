#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from django.core.exceptions import ObjectDoesNotExist

# from shinobi_api.serializers.report import ReportSerializer

__author__ = "hien"
__date__ = "07 18 2016, 10:12 AM"

import datetime
from rest_framework import status, exceptions
from rest_framework.response import Response

from shinobi_api import permissions
from shinobi_api.models import Terms, Privacy, Page
from shinobi_api.serializers import UserSerializer
from shinobi_api.services import UserService
from shinobi_api.services.utils import Utils
from django.utils.translation import ugettext_lazy as _

class CreateUserMixin(object):
    user_serialiser_class = UserSerializer

    def save(self, data, return_http=True):
        try:
            if 'is_active' not in data:
                data['is_active'] = False
            serializer = self.user_serialiser_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e


class UpdateUserMixin(object):
    def edit(self, current, id, data):
        user = UserService.get_user(id)
        if not user:
            raise exceptions.NotFound()
        if permissions.allow_access_user(current, user=user):
            serializer = UserSerializer(instance=user, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class ViewUserMixin(object):
    def get_user(self, id, **kwargs):
        user = UserService.get_user(id, **kwargs)
        if user is None:
            exceptions.NotFound()
        return user

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.get_user(int(pk), **request.query_params.copy())
        permissions.allow_access_user(request.user, user)
        serializer = UserSerializer(instance=user)
        return Response(serializer.data)


class ListUserMixin(object):
    def get_list(self, request, filter={}, **kwargs):
        kwargs['limit'] = int(request.query_params.get('limit', '20'))
        kwargs['offset'] = int(request.query_params.get('offset', '0'))
        kwargs['search'] = request.query_params.get('search', None)
        users = UserService.get_users(filter=filter, **kwargs)
        serializer = UserSerializer(instance=users['result'], many=True)
        return Response({
            'result': serializer.data,
            'count': users['count']
        })


# class ReportMixin(object):
#     """
#     Visitor's report
#     """
#
#     def report(self, request, *args, **kwargs):
#
#         # get building_id from request.user.building_id
#         user_id = kwargs.get('user_id') or request.user.id
#         fill = {}
#         data = request.data.copy()
#         fill['user_id'] = user_id
#         fill['is_disabled'] = False
#         building = Building.objects.filter(**fill).first()
#         if building is None:
#             raise exceptions.ParseError(_("There aren't activated location."))
#         building_id = building.pk
#         input_data = dict()
#         input_data['user_id'] = user_id
#         input_data['building_id'] = building_id
#         input_data['type'] = kwargs.get('type')
#         serializer = ReportSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             input_data['start_date'] = datetime.datetime.strptime(request.data['start_date'], '%Y-%m-%d').date()
#             input_data['end_date'] = datetime.datetime.strptime(request.data['end_date'], '%Y-%m-%d').date()
#         except Exception as e:
#             input_data['start_date'] = datetime.date.today()
#             input_data['end_date'] = datetime.date.today()
#
#         result = ReportService.report(input_data)
#         serializer = ReportSerializer(result['data'], many=True)
#         return Response({'data': serializer.data,
#                          'total': result['total']
#                          }, status=status.HTTP_200_OK)

class GetTermsMixin(object):
    def list(self, request, *args, **kwargs):
        terms = Terms.objects.first()
        return Response({
            'content': terms.content,
            'updated_at': terms.updated_at
        })


class GetPrivacyMixin(object):
    def list(self, request, *args, **kwargs):
        privacy = Privacy.objects.first()
        if not privacy:
            privacy = Privacy()
        return Response({
            'content': privacy.content,
            'updated_at': privacy.updated_at
        })


# class LocationMixin(object):
#     def get_location_id(self, request, **kwargs):
#         fill = {}
#         fill['user_id'] = request.user.id
#         fill['is_disabled'] = False
#         building = Building.objects.filter(**fill).first()
#         if building is None:
#             raise exceptions.ParseError(_("There aren't activated location."))
#         return building.pk

class PageMixin(object):

    def get_object(self, data, **kwargs):
        url = data['url']
        dom_origin = data['dom_origin']
        page = Page.objects(url=url, dom_origin=dom_origin)
        if page.count():
            return page
        else:
            return None
