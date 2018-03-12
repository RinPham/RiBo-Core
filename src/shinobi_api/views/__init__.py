#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 05, 2016 09:39:00 AM$"

from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    activity_log = True


from shinobi_api.views.auth import AuthViewSet
from shinobi_api.views.user import UserViewSet
from shinobi_api.views.geo import GeoViewSet
from shinobi_api.views.support import SupportViewSet
