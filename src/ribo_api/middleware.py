from django.conf import settings
from django.core.urlresolvers import resolve

from ribo_api.serializers import ClientSerializer
from ribo_api.services.utils import Utils
from ribo_api.services.vmsrequest import VMSRequest


class ApiMiddleware(object):
    """
    API middleware here
    """
    handling_apps = [settings.RIBO_API]
    logging_apps = [settings.RIBO_API]
    view = None
    view_kwargs = None

    def process_response(self, request, response):
        if resolve(request.path).app_name in self.logging_apps:
            self._log_data(request, response)
        return response

    def process_request(self, request):
        if resolve(request.path).namespace:
            setattr(request, 'version', resolve(request.path).namespace)
        if resolve(request.path).app_name in self.handling_apps:
            self._check_api_headers(request)
        request._body = request.body
        Utils.request = request

    # def process_view(self, request, view, *args, **kwargs):
    #     setattr(view, 'view_args', args)
    #     self.view = view

    def process_exception(self, request, exception):
        response = type('', (), {})()
        response.status_code = 500
        response.exception = response.content = exception
        self._log_data(request, response)

    def _check_api_headers(self, request):
        """
        Check request to make sure all header is valid
        :param request:
        :return: None
        """
        serializer = self._get_client_serialiser(request)
        if not serializer.is_valid():
            setattr(request, 'bad_request_header', serializer.errors)
        setattr(request, 'client', serializer.data)

    def _get_client_serialiser(self, request):
        """
        Get client serializer
        :param request:
        :return: ClientSerializer
        """
        data = {}
        data['ip'] = self._get_client_ip(request)
        data['device'] = request.META.get('HTTP_DEVICE')
        data['app_id'] = request.META.get('HTTP_APPID')
        data['type'] = request.META.get('HTTP_TYPE')
        data['language'] = request.META.get('HTTP_LANGUAGE', 'en')
        data['public_base'] = request.META.get('HTTP_PUBLIC')
        data['user_agent'] = self._get_user_agent(request)
        data['version'] = request.version
        return ClientSerializer(data=data)

    def _get_client_ip(self, request):
        """
        Get client ip
        :param request:
        :return: string ip
        """
        if request.META.get('HTTP_IP'):
            return request.META.get('HTTP_IP')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _get_user_agent(self, request):
        if 'HTTP_AGENT' in request.META:
            return request.META.get('HTTP_AGENT')
        return request.META.get('HTTP_USER_AGENT', '')

    def _log_data(self, request, response):
        url = (resolve(request.path_info))
        attrs = dict(
            request=request,
            url=url,
            view=self.view,
            response=response
        )
        VMSRequest.set_attrs(**attrs).log().reset()
