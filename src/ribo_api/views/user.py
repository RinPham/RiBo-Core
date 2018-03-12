
import os
from datetime import date
from os.path import join, exists

import boto
from PIL import Image, ImageOps
from boto.s3.key import Key
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.decorators import list_route
from rest_framework.response import Response

from shinobi_api import permissions
from shinobi_api.const import UserType
from shinobi_api.decorators import logging
from shinobi_api.mixins import UserLoginMixin
from shinobi_api.serializers import (
    UserSerializer, PasswordSerializer, PasswordResetSerialiser
)
from shinobi_api.services import UserService, EmailService, Utils
from shinobi_api.views import BaseViewSet
from shinobi_api.views.mixins import CreateUserMixin

AVATAR_CROPTED_SIZE = 250, 250


def crop_image(file_path, file_name):
    """
    Crop image to AVATAR_CROPTED_SIZE and save as JPEG format
    :param file_path:
    :param file_name:
    :return:
    """
    full_path = join(file_path, file_name)
    extension = file_name[file_name.rfind('.'):]
    new_file_name = file_name.replace(extension, '.resized.jpeg')
    new_full_path = join(file_path, new_file_name)
    im = Image.open(full_path)
    im = ImageOps.fit(im, AVATAR_CROPTED_SIZE, Image.ANTIALIAS)
    im.save(new_full_path, 'JPEG')
    os.remove(full_path)
    return new_file_name


def upload_origin(file_path, upload_dir, file_name):
    extension = file_name[file_name.rfind('.'):]
    new_file_name = file_name.replace(extension, '.origin.jpeg')
    full_path = join(file_path, file_name)
    new_full_path = join(file_path, new_file_name)
    img = Image.open(full_path)
    img.save(new_full_path, "JPEG", quality=80, optimize=True, progressive=True)
    if settings.DEBUG == False:
        sync_to_AWS3(new_full_path, upload_dir, new_file_name)


def handle_upload(request, base_path='avatars/%s', **kwargs):
    save_origin = kwargs.pop('save_origin', False)
    saved = dict()
    upload_dir = date.today().strftime(base_path)
    upload_full_path = join(settings.MEDIA_ROOT, upload_dir)

    if not exists(upload_full_path):
        os.makedirs(upload_full_path)

    for key, file in request.FILES.items():
        file_name = '{0}{1}_{2}'.format(Utils.id_generator(10), request.user.id, file.name)
        dest = open(os.path.join(upload_full_path, file_name), 'wb')
        for chunk in file.chunks():
            dest.write(chunk)
        dest.close()
        if save_origin:
            upload_origin(upload_full_path, upload_dir, file_name)
        file_name = crop_image(upload_full_path, file_name)
        file_dir = join(upload_dir, file_name)
        saved.update({key: file_dir})
        local_file_path = join(upload_full_path, file_name)
        # Sync uploaded file to S3
        if settings.DEBUG == False:
            sync_to_AWS3(local_file_path, upload_dir, file_name)
    return saved


def sync_to_AWS3(local_file_path, sync_path, file_name):
    try:
        upload_to = join(settings.MEDIAFILES_LOCATION, sync_path)
        bucket_name = settings.AWS_STATIC_BN
        s3_conn = boto.connect_s3(settings.AWS_ID, settings.AWS_SECRET)
        bucket = s3_conn.get_bucket(bucket_name)
        bucket_key = Key(bucket)
        bucket_key.key = join(upload_to, file_name)
        bucket_key.set_contents_from_filename(local_file_path)
        bucket_key.make_public()
        return True
    except Exception as e:
        return False


class UserViewSet(BaseViewSet, UserLoginMixin, CreateUserMixin):
    view_set = 'user'
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /user Create new user
        @apiName Create
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {string} email
        @apiParam {string} password
        @apiParam {string} [first_name]
        @apiParam {string} [middle_name]
        @apiParam {string} [last_name]
        @apiParam {object} profile
        @apiParam {number} [profile.gender] (0: male, 1: female)
        @apiParam {string} [profile.dob]
        @apiParam {file} [profile.avatar] upload file
        @apiParam {string} [profile.address1]
        @apiParam {string} [profile.address2]
        @apiParam {string} [profile.zip_code]
        @apiParam {string} [profile.city]
        @apiParam {string} [profile.home_phonenumber] Home phone
        @apiParam {string} [profile.mobile_phonenumber] Mobile phone

        @apiSuccess {object} user
        """
        data = request.data.copy()
        # data['user_type'] = UserType.MANAGER
        return self.save(data)

    @list_route(methods=['post'], permission_classes=())
    def verify(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /user/verify Validate user signup token
        @apiName Verify
        @apiGroup ~User Next version
        @apiPermission none

        @apiParam {string} token
        @apiParam {string} type

        @apiSuccess {object} user
        @apiSuccess {string} token
        @apiSuccess {string} appkey
        """
        token = request.data.get('token', None)
        type = request.data.get('type', 'activation')
        if not token:
            raise exceptions.ParseError(('Please provide token.'))

        if 'activation' == type:
            user_email = UserService.verify_email(token=token)
            if user_email is False:
                raise exceptions.ParseError(_('Invalid token.'))
            return self.response_login(id=user_email.user_id, client=request.client)

    @list_route(methods=['put', 'post'], permission_classes=())
    def password(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /user/password Set user password
        @apiName SetPassword
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {String} email
        @apiParam {string} [token]
        @apiParam {String} password or one_login_token
        @apiParam {String} new_password New password

        @apiSuccess 200 Password has been saved
        @apiError 401 Invalid authentication data
        """
        data = request.data.copy()
        serializer = PasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Your password has been updated"})

    @list_route(methods=['put'])
    @logging.ignore
    def avatar(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /user/avatar User set avatar
        @apiName UpdateAvatar
        @apiGroup ~User Next version
        @apiPermission IsAuthenticated

        @apiParam {File} avatar
        @apiSuccess avatar Path to avatar.
        @apiError Invalid file type, File not found.
        """
        if 'avatar' not in request.FILES:
            raise exceptions.ParseError(_('Please add a file.'))
        saved = handle_upload(request)
        data = {
            'id': request.user.id,
            'profile': {
                'avatar': saved['avatar']
            }
        }
        UserService.save(data)
        return Response(saved)

    @list_route(methods=['post', 'put','get'], permission_classes=(permissions.NotAuthenticated,))
    def reset_password(self, request):
        """
        @apiVersion 1.0.0
        @api {POST|PUT} /user/reset_password user forgot password
        @apiName ResetPassword
        @apiGroup ~User Next version
        @apiPermission none

        @apiParam {String} [email] Required if method POST
        @apiParam {string} [uid] Required if method PUT
        @apiParam {string} [token] Required if method PUT
        @apiParam {string} [password] Required if method PUT

        @apiSuccess [200]
        """
        if request.method == 'PUT':
            return self.check_reset_password(request)
        elif request.method == 'POST':
            return self.send_reset_password_link(request)
        else:
            return self.check_reset_link(request)

    # tutrinhcg: add reset passcode --start
    @list_route(methods=['post', 'put'], permission_classes=(permissions.NotAuthenticated,))
    def reset_pass_code(self, request):
        """
        @apiVersion 1.0.0
        @api {POST|PUT} /user/reset_pass_code User forgot password
        @apiName ResetPassword
        @apiGroup VMS_API Account
        @apiPermission none

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Non Authenticate Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": 1,
            "Agent": "Samsung A5 2016, Android app, build_number other_info"
        }

        @apiParam {String} [email] Required if method POST
        @apiParam {String} [answer1] Required if method POST
        @apiParam {String} [answer2] Required if method POST
        @apiParam {String} [answer3] Required if method POST
        @apiParam {string} [uid] Required if method PUT
        @apiParam {string} [token] Required if method PUT
        @apiParam {string} [password] Required if method PUT

        @apiSuccess {string}[username] if method POST
        @apiSuccess {string}[token] if method POST
        @apiSuccess {string}[uid] if method POST
        @apiSuccess {string}[message] if method PUT
        """
        if request.method == 'PUT':
            return self.check_reset_password(request)
        else:
            if self.check_question(request):
                return self.send_reset_pass_code(request)
            else:
                raise exceptions.ParseError(_('wrong answer.'))

    # def check_question(self, request):
    #     data = request.data.copy()
    #     email = data.get('email', None)
    #     if not email:
    #         raise exceptions.ParseError(_('Please provide email.'))
    #     user = UserService.get_by_email(email)
    #     question1 = QuestionReset.objects.get(user_id=user.pk, number_question=1)
    #     question2 = QuestionReset.objects.get(user_id=user.pk, number_question=2)
    #     question3 = QuestionReset.objects.get(user_id=user.pk, number_question=3)
    #
    #     if data['answer1'] == question1.answer and data['answer2'] == question2.answer \
    #             and data['answer3'] == question3.answer:
    #         return True
    #     else:
    #         return False

    def send_reset_pass_code(self, request):
        data = request.data.copy()
        email = data.get('email', None)
        if not email:
            raise exceptions.ParseError(_('Please provide email.'))
        user = UserService.get_by_email(email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return Response({
            'uid': uid.decode('utf-8'),
            'token': token,
            'username': user.email
        })

    # tutrinhcg: add reset passcode --end

    def check_reset_link(self, request):
        data = request.data.copy()
        user = self.get_user(uidb64=data['uid'])
        if not user:
            raise exceptions.ParseError(_('Invalid user.'))
        if not self.valid_token(user, data['token']):
            raise exceptions.ParseError(_('Invalid token.'))
        return Response()

    def send_reset_password_link(self, request):
        email = request.data.get('email', None)
        if not email:
            raise exceptions.ParseError(_('Please provide email.'))
        user = UserService.get_by_email(email)
        if not user:
            raise exceptions.NotFound(_('User not found.'))
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        EmailService.reset_link(token=token, uid=uid, user=user)
        return Response({"message": "A link with instruction has been sent to your email, please check your email to reset password."})

    def check_reset_password(self, request):
        serializer = PasswordResetSerialiser(data=request.data.copy())
        serializer.is_valid(raise_exception=True)
        user = self.get_user(uidb64=serializer.data['uid'])
        if not user:
            raise exceptions.ParseError(_('Invalid user.'))
        if not self.valid_token(user, serializer.data['token']):
            raise exceptions.ParseError(_('Invalid token.'))
        user.set_password(serializer.data['password'])
        user.save()
        return Response({"message": "Your password has been updated"})

    def get_user(self, *args, **kwargs):
        """Get user base on uidb64
        :return: User
        """
        uidb64 = kwargs.get('uidb64')
        uid = urlsafe_base64_decode(uidb64)
        return UserService.get_user(uid)

    def valid_token(self, user, token):
        """
        Check user token
        :param User user:
        :param string token:
        :return: boolean
        """
        return user is not None and default_token_generator.check_token(user, token)
