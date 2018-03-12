#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 05, 2016 2:29:54 PM$"

import time
import hashlib

from django.db import transaction
from django.db.models import Q

from shinobi_api.services.utils import Utils
from shinobi_api.services.base import BaseService
from shinobi_api.services.vmscache import VMSCacheService
from shinobi_api.services.geo import GeoService
from rest_framework import exceptions
from shinobi_api.models import (
    User, UserPref, UserEmail, Api, UserProfile, UserMedia
)
from shinobi_api.const import (
    UserType, ResourceType
)
import re
from shinobi_api.services.auth import AppKeyService

class UserError(TypeError): pass  # base exception class


class UserService(BaseService):
    @classmethod
    def _get_cache_service(cls):
        return VMSCacheService.factory(ResourceType.RS_USER)

    @classmethod
    def get_user(cls, user_id, create_new=False, **kwargs):
        try:
            cache_service = cls._get_cache_service()
            cached_user = cache_service.get(user_id)
            if (cached_user):
                user = cached_user
                if not user.profile:
                    try:
                        user_profile = UserProfile.objects.get(pk=user_id)
                    except:
                        # Not exist
                        user_profile = UserProfile()
                        user_profile.user_id = user.id
                        user_profile.save()
                    user.profile = user_profile
            else:
                user = User.objects.get(pk=user_id)
                try:
                    user_profile = UserProfile.objects.get(pk=user_id)
                except:
                    # Not exist
                    user_profile = UserProfile()
                    user_profile.user_id = user.id
                    user_profile.save()
                user.profile = user_profile
                cache_service.set(user_id, user)
        except Exception as e:
            cls.log_exception(e)
            if create_new:
                user = User()
                return user
            else:
                return None
        includes = kwargs.get('includes', [])
        return user
    
    @classmethod
    def _post_update_user(cls, id):
        cache_service = cls._get_cache_service()
        cache_service.delete(id)

    @classmethod
    def delete_user(cls, user_id):
        with transaction.atomic():
            try:
                user = User.objects.get(pk=user_id)
            except:
                return None
            cls._post_update_user(user.id)
            UserEmail.objects.filter(user_id=user.id).delete()
            Api.objects.filter(user_id=user.id).delete()
            UserProfile.objects.filter(user_id=user.id).delete()
            UserPref.objects.filter(user_id=user.id).delete()
            UserMedia.objects.filter(user_id=user.id).delete()
            user.delete()
            return True

    @classmethod
    def delete_user_by_email(cls, email):
        user = User.objects.filter(email=email).first()
        if user:
            cls.delete_user(user.id)

    @classmethod
    def lock_user(cls, user_id):
        #TODO: Update models to support this, update LOGIN to check this
        try:
            user = User.objects.get(pk=user_id)
        except:
            return None
        user.lock = True
        user.locked_at = int(time.time())
        user.save()
        return True

    @classmethod
    def suspended_user(cls, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except:
            return None
        user.is_active = False
        user.save()
        return True

    @classmethod
    def force_change_pass(cls, user_id, force=1):
        try:
            profile = UserProfile.objects.get(user_id=user_id)
            profile.force_change_pass = force
            profile.save()
            # Reset cache
            cache_service = cls._get_cache_service()
            cache_service.delete(user_id)
        except Exception as e:
            cls.log_exception(e)
            return None
        return True

    """
        user_data={
            'first_name': "name",
            'middle_name': '',
            'last_name': "name",
            'user_tz': 'US/Pacific',
            "email":"email@example.com",
            "password":"plain_password",
            "manager_id", "Required if in (UserType.MANAGER)",
            "user_type" : UserType.GUEST ...,
            "profile": {
                "gender": Gender.MALE | Gender.FEMALE
                "dob": "Date of birth",
                "NPI": ""
            }
        }
    """

    @classmethod
    def save(cls, user_data, **kwargs):
        from shinobi_core.utilstz import location_to_tz
        with transaction.atomic():
            add_new = True
            profile_data = user_data.pop('profile')
            password = user_data.pop('password', None)
            user_email = user_data.get('email', None)
            if user_data.get("id"):
                user = cls.get_user(user_data['id'])
            else:
                user = None
            if user is not None:
                add_new = False
                profile = user.profile
            else:
                user = User()
            current_email = user.email
            # All data must be validated at serializer tier
            for key in user_data:
                setattr(user, key, user_data[key])
            # Set first password
            if add_new:
                if not password and not user.password:
                    password = Utils.id_generator(8)
                user.set_password(password)
            user.save()
            if not user.email:
                user.email = "{0}@{1}".format(str(user.id), "smartoffice.vn")
                user.save()
            if add_new:
                profile = UserProfile()
                profile.user_id = user.id
            for key in profile_data:
                setattr(profile, key, profile_data[key])
            profile.save()
            location_id = profile.location_id
            location = GeoService.get_location(location_id)
            if location:
                location_tz = location_to_tz(location.country,location.admin1_code)
                if location_tz:
                    user_data['user_tz'] = location_tz
            send_verify_email = True
            # if user.user_type == UserType.MANAGER:
            #     cls.save_manager(user, add_new, **user_data)
            # if user.user_type == UserType.GUEST:
            #     cls.save_visitor(user, add_new, **user_data)
            #     send_verify_email = False
            if user_email != current_email:
                cls.add_email(user.id, user.email, current_email=current_email, is_primary=True, password=password, send_verify_email=send_verify_email)
            if not add_new:
                # Reset cache
                cache_service = cls._get_cache_service()
                cache_service.delete(user.id)
            return cls.get_user(user.id)

    @classmethod
    def save_manager(cls, user, add_new, **kwargs):
        """
        Save extends data for manager
        :return:
        """
        if add_new:
            user.manager_id = user.id
            user.save()

    @classmethod
    def save_visitor(cls, user, add_new, **kwargs):
        pass

    @classmethod
    def activate_user(cls, attrs):
        key = re.sub('[^0-9a-zA-Z]+', '', attrs.get('key'))
        pin = attrs.get('pin')
        appkey = AppKeyService.get(key)
        if not appkey:
            raise exceptions.AuthenticationFailed()
        user = appkey.user
        user.set_password(pin)
        user.save()
        UserService._post_update_user(user.id)
        if not appkey.is_activated():
            appkey.activate()
        return attrs
    
    @classmethod
    def add_email(cls, user_id, new_email, **kwargs):
        """
        Return current email address or create new instance
        :return: UserEmail
        """
        is_primary = kwargs.pop('is_primary', False)
        password = kwargs.pop('password', False)
        send_verify_email = kwargs.pop('send_verify_email', False)
        try:
            user_email = UserEmail.objects.get(email=new_email)
            if user_email.user_id == 0 and user_id > 0:
                # This email has added before, but no one hold
                user_email.user_id = user_id
                user_email.is_primary = True
                user_email.save()
                if user_email.verified_at == 0 and send_verify_email:
                    # This email has added to user_email, but not verified
                    cls.send_verify(token=user_email.token, email=new_email, password=password)
        except UserEmail.DoesNotExist:
            token = cls.gen_token(new_email)
            user_email = UserEmail()
            user_email.user_id = user_id
            user_email.email = new_email
            user_email.is_primary = is_primary
            user_email.created_at = int(time.time())
            user_email.token = token
            user_email.save()
            if send_verify_email:
                # Add this param to avoid send many verify/confirm mail
                cls.send_verify(token=token, email=new_email, password=password)
        except Exception as e:
            return None

        current_email = kwargs.pop('current_email', None)
        if user_id > 0 and current_email and new_email != current_email:
            # Set other email address of current user to be secondary
            UserEmail.objects.exclude(id=user_email.id) \
                .filter(user_id=user_id).update(is_primary=0)
        return user_email

    @classmethod
    def send_verify(cls, **kwargs):
        from .email import EmailService
        EmailService.verify_email(
            token=kwargs.pop('token'),
            email_add=kwargs.pop('email'),
            password=kwargs.pop('password'),
            template=kwargs.pop('template', 'verify')
        )

    @classmethod
    def is_verified_email(cls, email, **kwargs):
        try:
            email = UserEmail.objects.get(email=email)
            if kwargs.pop('get_timestamp', None) is not None:
                return email.verified_at > 0
            else:
                return email.verified_at
        except Exception as e:
            return False



    @classmethod
    def get_email(cls, email):
        try:
            user_email = UserEmail.objects.get(email=email)
            if user_email:
                return user_email
        except Exception as e:
            cls.log_exception(e)
            return None
        return None

    @classmethod
    def verify_email(cls, **kwargs):
        token = kwargs.pop('token', None)
        try:
            if token is not None:
                user_email = UserEmail.objects.get(token=token)
                user_email.is_primary = True
            elif kwargs.get('email_id', False) is not False:
                user_email = UserEmail.objects.get(pk=kwargs.pop('email_id'))
            user_email.verified_at = int(time.time())
            user_email.token = cls.gen_token(user_email.user_id)
            user_email.save()
            user = User.objects.get(id=user_email.user_id)
            user.is_active = True
            user.save()
            return user_email
        except UserEmail.DoesNotExist:
            return False
        except Exception as e:
            cls.log_exception(e)
        return False

    @classmethod
    def gen_token(cls, user_id):
        text = str(user_id) + Utils.id_generator(10) + str(int(time.time()))
        hash_object = hashlib.md5(text.encode('utf-8'))
        return hash_object.hexdigest()

    @classmethod
    def get_by_email(cls, email):
        try:
            user = User.objects.get(email=email)
            return cls.get_user(user.pk)
        except User.DoesNotExist:
            return None

    @classmethod
    def get_users(cls, *args, **kwargs):
        limit = kwargs.get('limit', 20)
        offset = kwargs.get('offset', 0)
        search = kwargs.get('search', None)
        end = offset + limit
        filter = kwargs.get('filter', {})
        order_by = kwargs.get('order', '-id')
        id_only = kwargs.get('id_only', False)
        includes = kwargs.get('includes', [])
        excludes = kwargs.get('excludes', {})
        users = []
        if search:
            term = Q(first_name__icontains=search) | Q(middle_name__icontains=search)
            user_ids = User.objects.values_list('id', flat=True) \
                        .order_by(order_by).filter(**filter).filter(term)[offset:end]
            count = User.objects.values_list('id', flat=True) \
                        .order_by(order_by).filter(**filter).filter(term).count()
        else:
            user_ids = User.objects.values_list('id', flat=True).order_by(order_by).filter(**filter).exclude(**excludes)[offset:end]
            count = User.objects.values_list('id', flat=True).order_by(order_by).filter(**filter).exclude(**excludes).count()
        if id_only:
            return user_ids
        for id in user_ids:
            users.append(cls.get_user(id, includes=includes))
        return {
            'result': users,
            'count': count
        }
