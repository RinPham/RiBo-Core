from django.conf.urls import url, include
from rest_framework import routers
from ribo_api.views import UserViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'user', UserViewSet, base_name='UserView')

urlpatterns = [
    url(r'^', include(router.urls)),
]
