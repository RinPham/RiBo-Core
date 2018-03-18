from django.conf import settings
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api.services.api import ApiService
from ribo_api.services.oauth import OauthService
from ribo_api.services.utils import Utils


class AuthViewSet(ViewSet):
    permission_classes = ()

    @list_route(methods=['get'])
    def token(self, request, *args, **kwargs):
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
        try:
            code = request.GET['code']
            redirect_uri = Utils.get_public_url('/api/v1/auth/token')
            credentials = OauthService.get_credentials(code, redirect_uri)
            json = credentials.to_json()
            data = ApiService.create_token(json)
            return Response(data)
        except Exception as e:
            Utils.log_exception(e)
            raise e