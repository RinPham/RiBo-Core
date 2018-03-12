#! /usr/bin/python
#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "trung"
__date__ = "$Oct 25, 2016 12:01:41 PM$"

from rest_framework.response import Response

from shinobi_api.models.faq import Faq
from shinobi_api.serializers.faq import FaqSerializer
from shinobi_api.services.email import EmailService
from shinobi_api.views import BaseViewSet


class SupportViewSet(BaseViewSet):
    view_set = 'support'
    permission_classes = ()
    authentication_classes = ()

    def list(self, request):
        """
        @apiVersion 1.0.0
        @api {GET} /support List FAQ
        @apiName ListFAQ
        @apiGroup ~Support Next version
        @apiPermission none

        @apiSuccess {object[]} list_faq
        @apiSuccess {number} list_faq.id
        @apiSuccess {string} list_faq.question
        @apiSuccess {string} list_faq.answer
        """
        res = FaqSerializer(Faq.objects.all(), many=True).data
        return Response(dict(list_faq=res))

    def create(self, request):
        """
        @apiVersion 1.0.0
        @api {POST} /support Create support ticket
        @apiName Create
        @apiGroup ~Support Next version
        @apiPermission none

        @apiParam {string} name
        @apiParam {string} email
        @apiParam {string} message

        @apiSuccess {boolean} success
        """
        EmailService.support_ticket(**request.data.dict())
        return Response(dict(success=True))
