#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 05, 2016 3:41:30 PM$"

import logging
import json

from django.contrib.auth import user_logged_in
from django.http import QueryDict
from shinobi_api.services.utils import Utils
from rest_framework import status

from shinobi_api.models import UserActivityLog

logger = logging.getLogger("project")


def listener_logged_in(sender, user=None, **kwargs):
    VMSRequest.user_id = user.id


user_logged_in.connect(listener_logged_in)


class VMSRequest(object):
    ENV_HEADERS = (
        'X-Varnish',
        'X-Request-Start',
        'X-Heroku-Queue-Depth',
        'X-Real-Ip',
        'X-Forwarded-Proto',
        'X-Forwarded-Protocol',
        'X-Forwarded-Ssl',
        'X-Heroku-Queue-Wait-Time',
        'X-Forwarded-For',
        'X-Heroku-Dynos-In-Use',
        'X-Forwarded-For',
        'X-Forwarded-Protocol',
        'X-Forwarded-Port',
        'Runscope-Service'
    )
    enable_activity_log = True
    user_id = None
    request = None
    url = None
    view = None
    response = None

    @classmethod
    def set_attrs(cls, **kwargs):
        for key in kwargs:
            setattr(cls, key, kwargs[key])
        return cls

    @classmethod
    def reset(cls):
        cls.enable_activity_log = True
        cls.user_id = None

    @classmethod
    def get_user_id(cls):
        if cls.user_id:
            return cls.user_id
        if cls.request.user and cls.request.user.is_authenticated():
            return cls.request.user.id
        return 0

    @classmethod
    def get_view_name(cls):
        name = cls.url.url_name.split('-')
        return name[0]

    @classmethod
    def log_debug(cls):
        method = cls.request.method.upper()
        error = '%s %s %s %s %s <<%s>>' % (
            cls.request.client.get('ip'),
            cls.get_user_id(),
            method,
            cls.response.status_code,
            cls.request.get_full_path(),
            cls.response.content
        )
        logger.error(error)

    @classmethod
    def get_request_body(cls):
        method = cls.request.method.upper()
        request = cls.request
        if method == "PUT":
            return QueryDict(request._body).copy()
        if method == "GET":
            return request.GET.copy()
        return request.POST.copy()

    @classmethod
    def get_meta(cls):
        meta = {}
        post_data = cls.get_request_body()
        if post_data:
            meta['p'] = post_data
        return json.dumps(meta)

    @classmethod
    def log_activity(cls, **kwargs):
        from django.utils import timezone
        user_id = kwargs['user_id'] if 'user_id' in kwargs else cls.get_user_id()
        action = kwargs['action'] if 'action' in kwargs else cls.request.method
        view = kwargs['view'] if 'view' in kwargs else cls.get_view_name()
        ip = cls.request.client['ip']
        url=cls.request.get_full_path()
        status=cls.response.status_code
        #meta=cls.get_meta()
        meta = None
        #By hien@codeographer.net: Disable log meta, I noticed we logging the pin in plain
        device_type = cls.request.META.get('HTTP_TYPE', 0)
        ft = dict(ip=ip, action=action,url=url,status=status,user_id=user_id, meta=meta)
        if action in ["GET"]:
            exist_activity = UserActivityLog.objects.filter(**ft).order_by("-id").first()
            if exist_activity:
                exist_activity.latest_at = timezone.now()
                exist_activity.save()
                return
        data = dict(
            ip=ip,
            user_id=user_id,
            action=action,
            meta="",
            url=url,
            device_type=device_type,
            status=status
        )
        UserActivityLog.objects.create(**data)

    @classmethod
    def log(cls):
        try:
            client_error = status.is_client_error(cls.response.status_code)
            server_error = status.is_server_error(cls.response.status_code)
            # Debug log for client errors or server errors
            if client_error or server_error:
                cls.log_debug()

            # Activity log for users
            # if not client_error and not server_error and cls.get_user_id():
            if cls.get_user_id() and hasattr(cls.view, 'cls'):
                _cls = getattr(cls.view, 'cls')
                if getattr(_cls, 'activity_log', True) and not getattr(cls.request, 'ignore_activity_log', False):
                    cls.log_activity()
        except Exception as e:
            print (str(e))
        return cls
