#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "hien"
__date__ = "09 21 2015, 2:11 PM"

import string

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework import exceptions
from shinobi_api.serializers import ServiceSerializer, serializers
from shinobi_api.const import UserType
from shinobi_api.models import UserProfile, User
from shinobi_api.services import (
    UserService, TokenAuthService
)


class ValidatePasswordMixin(object):
    def validate_password_value(self, value):
        """
        Validate new password,
        :param value:
        :return:
        """
        if value:
            # check password length
            pw_length = 6
            if len(value) < pw_length:
                raise serializers.ValidationError(_('Password must be at least %d characters.') % pw_length)
            contains_number = False
            contains_upper = False
            contains_lower = False
            is_ascii = True
            for char in value:
                if char.isdigit():
                    contains_number = True
                if char.isupper():
                    contains_upper = True
                if char.islower():
                    contains_lower = True
                if char not in (string.ascii_letters + string.digits + string.punctuation):
                    is_ascii = False
            if not is_ascii:
                raise serializers.ValidationError(_('Only allow ascii characters for password.'))

            if not ((contains_lower or contains_upper) and contains_number):
                raise serializers.ValidationError(
                    _('Password must contains at least one character and number.')
                )
            return value


class PasswordSerializer(serializers.Serializer, ValidatePasswordMixin):
    """
    This serializer use for input and valid when user change password
    """
    email = serializers.EmailField(required=False)
    token = serializers.CharField(required=False)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate_new_password(self, value):
        password = self.initial_data.get('password')
        if password == value:
            detail = 'New password should be different from current password.'
            raise exceptions.ValidationError(detail=detail, )
        return self.validate_password_value(value)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        token = attrs.get('token', None)
        user = None
        detail = None
        # Authenticate by one-click-login token
        if token:
            user = TokenAuthService.check_token(token, return_user=True)
        # Authenticate by email and old password
        if email and password:
            detail = 'You input wrong current password'
            try:
                # Get  from model, don't get from cache
                user = User.objects.get(email=email)
            except Exception as e:
                user = None
            if not user or not user.check_password(password):
                user = None
        if user:
            user.set_password(new_password)
            user.save()
            attrs['user'] = user
            return attrs
        else:
            if detail:
                raise exceptions.NotAuthenticated(detail=detail)
            else:
                raise exceptions.NotAuthenticated()


class CreatePasswordSerializer(serializers.Serializer, ValidatePasswordMixin):
    """
    This serializer use for input and valid when user create password
    """
    email = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    confirm_password = serializers.CharField(required=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate_new_password(self, value):
        return self.validate_password_value(value)

    def validate(self, attrs):
        email = attrs.get('email')
        confirm_password = attrs.get('confirm_password')
        new_password = attrs.get('new_password')
        user_id = attrs.get('user_id')
        if (email or user_id) and confirm_password and new_password:
            if email:
                user = UserService.get_by_email(email)
            elif user_id:
                user = UserService.get_user(user_id)
            if user:
                user.set_password(new_password)
                user.save()
                attrs['user'] = user
                return attrs
            else:
                raise exceptions.ValidationError(_('User not found.'))
        else:
            raise exceptions.ValidationError(_('Must include password.'))


class PasswordResetSerialiser(serializers.Serializer, ValidatePasswordMixin):
    uid = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    token = serializers.CharField(required=True)

    def validate_password(self, value):
        return self.validate_password_value(value)


class UserProfileSerializer(serializers.ModelSerializer):
    def get_avatar_url(self, avatar):
        if not avatar:
            avatar = 'avatars/default.png'
        if settings.DEBUG:
            avatar = 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT, settings.MEDIA_URL, avatar)
        else:
            avatar = '%s%s' % (settings.MEDIA_URL, avatar)
        return avatar

    def to_representation(self, instance):
        data = super(UserProfileSerializer, self).to_representation(instance)
        data['avatar'] = self.get_avatar_url(data['avatar'])
        return data

    class Meta:
        model = UserProfile
        fields = (
            'gender', 'dob', 'avatar', 'msg_indicator', 'NPI',
            'address1', 'address2', 'zip_code', 'city', 'location_id',
            'home_phonenumber', 'mobile_phonenumber'
        )
        read_only_fields = ('user_id',)

class UserSerializer(ServiceSerializer, ValidatePasswordMixin):
    profile = UserProfileSerializer(many=False)
    password = serializers.CharField(required=True, min_length=6)
    email = serializers.EmailField(required=True, max_length=254)
    #visitor = VisitorSerialiser(many=False, required=False)

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        if 'password' in ret:
            del ret['password']
        #if not instance.is_visitor and 'visitor' in ret:
        #    del ret['visitor']
        return ret

    # def validate_user_type(self, value):
    #     # TODO: Not allow user set themself to admin or staff
    #     if not UserType.is_valid_type(value):
    #         raise exceptions.ValidationError(_('Invalid user type.'))
    #     return value

    def validate_email(self,value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        if user:
            raise exceptions.ValidationError(_('Email already exists.'))


    def validate_password(self, value):
        return self.validate_password_value(value)

    def validate(self, attrs):
        # TODO: Validate visitor_data here
        return attrs

    def create(self, validated_data):
        try:
            for key in ['groups', 'user_permission']:
                if key in validated_data:
                    del validated_data[key]
            user = UserService.save(validated_data)
            return user
        except Exception:
            raise exceptions.APIException()

    def update(self, instance, validated_data):
        data = self.data
        for key in validated_data:
            data[key] = validated_data[key]
        # Not save password in this step
        if 'password' in data:
            del data['password']
        return UserService.save(data)

    class Meta:
        model = User
        read_only_fields = ('id',)
        fields = (
            'id', 'email', 'first_name', 'middle_name', 'last_name',
            'profile',
            'password',
            #'date_joined', 'visitor',
            'date_joined',
            'is_superuser', 'is_staff'
        )
        extra_kwargs = {'password': {'write_only': True, 'hidden': True}}
