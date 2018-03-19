from django.conf import settings
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api.services.api import ApiService
from ribo_api.services.oauth import OauthService
from ribo_api.services.utils import Utils


class AuthViewSet(ViewSet):
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /auth Login
        @apiName Login
        @apiGroup Ribo_api Authorization
        @apiPermission none

        @apiParam {string} code

        @apiSuccess {object} user + token
        @apiSuccessExample
        {
            "token": QL7RXWUJKDIISITBDLPRUPQZAXD81XYEHZ4HPL5J
            "user": {
                "email": thqbop@gmail.com
                "first_name": Quoc
                "last_name": Truong
                "avatar": https://lh3.googleusercontent.com/-pQMo5QOCrZo/AAAAAAAAAAI/AAAAAAAAAAc/bAFfAAB22cY/s96-c/photo.jpg
            }
        }
        """
        try:
            code = request.GET['code']
            redirect_uri = Utils.get_public_url('/api/v1/auth')
            credentials = OauthService.get_credentials(code, redirect_uri)
            json = credentials.to_json()
            data = ApiService.create_token(json)
            return Response(data)
        except Exception as e:
            Utils.log_exception(e)
            raise e