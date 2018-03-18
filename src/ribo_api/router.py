from django.conf.urls import url, include
from rest_framework import routers
from ribo_api.views import UserViewSet
from ribo_api.views.api.events import EventViewSet
from ribo_api.views.api.task import TaskViewSet
from ribo_api.views.auth import AuthViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'auth', AuthViewSet, base_name='AuthView')
router.register(r'user', UserViewSet, base_name='UserView')
router.register(r'task', TaskViewSet, base_name='TaskView')
router.register(r'event', EventViewSet, base_name='EventView')

urlpatterns = [
    url(r'^', include(router.urls)),
]
