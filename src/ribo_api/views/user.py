from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api.models.user import User
from ribo_api.serializers import UserSerializer
from ribo_api.services.api import ApiService
from ribo_api.services.oauth import OauthService
from ribo_api.services.utils import Utils


class UserViewSet(ViewSet):
    view_set = 'user'
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            ApiService.create_token(user_id=user.id,api_data=data)
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    @list_route(methods=['put'])
    def edit(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            user = User.objects(email = data.get('email', None))[0]
            serializer = self.serializer_class(user, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e
