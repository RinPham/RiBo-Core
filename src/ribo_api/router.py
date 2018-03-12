from django.conf.urls import url, include
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)


urlpatterns = [
    url(r'^', include(router.urls)),
]
