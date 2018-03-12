from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.not_authorized, name='403'),
    url(r'^api/v1/', include('shinobi_api.router', namespace='v1', app_name=settings.SHINOBI_API)),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.DOC_URL, document_root=settings.DOC_ROOT)
if settings.DEBUG404:
    urlpatterns += patterns('django.views.static', (r'^docs/(?P<path>.*)',
                                                    'serve', {'document_root': settings.DOC_ROOT}), )
