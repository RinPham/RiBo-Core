#! /usr/bin/python

#! /usr/bin/python
#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Oct 7, 2016 10:16:08 AM$"

from shinobi_api.services.base import BaseService
from shinobi_api.services.vmscache import VMSCacheService
from shinobi_api.models import (
    SystemMeta, AppMeta
)
from shinobi_api.const import (
    ResourceType
)
import json
from django.db import transaction
from django.utils import timezone
from shinobi_api.services.utils import Utils
from django.core.exceptions import ObjectDoesNotExist


LATEST_APP_KEY = "__latest__"

class MSystemError(TypeError): pass  # base exception class

class MSystemService(BaseService):
    
    @classmethod
    def _get_cache_service(cls):
        return VMSCacheService.factory(ResourceType.RS_APP);

    @classmethod
    def get_app(cls, version, *args, **kwargs):
        try:
            cache_service = cls._get_cache_service()
            cached_app = cache_service.get(version)
            if(cached_app):
                sys_app = cached_app
            else:
                sys_app = SystemMeta.objects.get(version=version)
                cache_service.set(version, sys_app)
        except ObjectDoesNotExist:
            return None
        return sys_app

    @classmethod
    def get_app_by_id(cls, id):
        sys_app = SystemMeta.objects.get(id=id)
        return cls.get_app(sys_app.version)
    
    @classmethod
    def get_user_app(cls, user_id):
        try:
            user_app = AppMeta.objects.get(user_id=user_id)
            if user_app.sensor_meta:
                user_app.sensor_meta = json.loads(user_app.sensor_meta)
        except ObjectDoesNotExist:
            return None
        return user_app


    @classmethod
    def get_latest(cls):
        try:
            cache_service = cls._get_cache_service()
            cached_app = cache_service.get(LATEST_APP_KEY)
            if cached_app:
                return cached_app
            return SystemMeta.objects.get(is_latest=1)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def delete_app(cls, id):
        try:
            sys_app = SystemMeta.objects.get(pk=int(id))
            cls._post_update(sys_app.version)
            if sys_app.is_latest:
                cls._post_update(LATEST_APP_KEY)
            sys_app.delete()
            return True
        except ObjectDoesNotExist:
            return False
    @classmethod
    def _post_update(cls, version):
        cache_service = cls._get_cache_service()
        cache_service.delete(version)
    """
    app_data = {
        'id': <id>,
        'version': 'version code'
        'version_name': 'app long name',
        'changes': "<app changes>"
        'available_at': "<date>"
        'is_latest': TRUE|FALSE
        'is_force_updated': TRUE|FALSE
    }
    """

    @classmethod
    def save(cls, app_data):
        try:
            sys_app = False
            add_new = True
            if app_data.get('id'):
                add_new = False
                sys_app = SystemMeta.objects.get(pk=int(app_data.get('id')))
            else:
                sys_app = SystemMeta(**app_data)
            if not add_new:
                sys_app.updated_at = timezone.now()
            if app_data.get("is_latest", None):
                SystemMeta.objects.all().update(is_latest=0)
                cls._post_update(LATEST_APP_KEY)
            sys_app.save()
            # Reset cache
            cls._post_update(sys_app.version)
            return sys_app
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_apps(cls, *args, **kwargs):
        try:
            filters = {}
            apps = []
            app_rs = SystemMeta.objects.values_list('version', flat=True).filter(**filters)
            for _app_version in app_rs:
                app = cls.get_app(_app_version)
                if app:
                    apps.append(app)
            return apps
        except Exception as e:
            cls.log_exception(e)
        return None
    
    @classmethod
    def sync_user_app(cls, user_id, *args, **kwargs):
        try:
            version = kwargs.get("version","")
            current_user_app = cls.get_user_app(user_id)
            if not current_user_app:
                current_user_app = AppMeta()
                current_user_app.user_id = user_id
            if current_user_app.version != version:
                current_user_app.version = version
                current_user_app.last_updated = timezone.now()
            current_user_app.save()
            return current_user_app
        except Exception as e:
            cls.log_exception(e)
        return None
    
    @classmethod
    def validate_user_app(cls, user_id, *args, **kwargs):
        version = kwargs.get("version","")
        if version:
            version = version[0]
        app_info = {
            "force_updated": 0,
            "message": "",
            "user": version,
            "current": ""
        }
        params = {
            "version": version,
        }
        try:
            user_app = cls.get_app(version)
            cls.sync_user_app(user_id, **params)
            latest_app = cls.get_latest()
            app_info['current'] = latest_app.version
            if latest_app.version != version:
                #Not matching latest version
                if latest_app.is_force_updated or not user_app:
                    app_info['force_updated'] = 1
                    app_info ["message"] = "You must update your app to continue"
                    app_info ["changes"] = latest_app.changes
        except Exception as e:
            cls.log_exception(e)
            app_info ["message"] = str(e)
        return app_info