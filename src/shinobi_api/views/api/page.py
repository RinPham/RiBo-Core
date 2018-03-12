from rest_framework.response import Response
from rest_framework.decorators import list_route
from shinobi_api.views import BaseViewSet
from shinobi_api.views.mixins import PageMixin
from shinobi_api.models import Page, Element
from shinobi_api.serializers.page import PageSerializer, ElementSerializer
from shinobi_api.upload_file import convertBase64toImg
from shinobi_api.serializers.page_technology import PageTechnologySerializer
import os
from django.conf import settings
from shinobi_api.services.page import PageService


def get_image_url(image):
    if not image:
        image = 'image/default.png'
    if settings.DEBUG:
        image = 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT, settings.MEDIA_URL, image)
    else:
        image = '%s%s' % (settings.MEDIA_URL, image)
    return image


class PageView(BaseViewSet, PageMixin):
    view_set = 'page-view'
    # login to send
    # permission_classes = (permissions.IsAuthenticated,)
    # not need login
    permission_classes = ()
    serializer_class = PageSerializer

    def create(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /page create page
        @apiName Post send data
        @apiGroup shinobi_api
        @apiPermission IsAuthenticated
        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Authenticated Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": "1",
            "Agent": "Samsung A5 2016, Android app, build_number other_info",
            "Authorization": "token QS7VF3JF29K22U1IY7LAYLNKRW66BNSWF9CH4BND"
        }
        @apiParams {string} url
        @apiParams {string} dom
        @apiParams {string} full_screen
        @apiParams {object[]} listElement

        @apiSuccess {json} result
        """
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /page/<id> get page
        @apiName Post send data
        @apiGroup shinobi_api
        @apiPermission IsAuthenticated
        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Authenticated Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": "1",
            "Agent": "Samsung A5 2016, Android app, build_number other_info",
            "Authorization": "token QS7VF3JF29K22U1IY7LAYLNKRW66BNSWF9CH4BND"
        }

        @apiSuccess {json} result
        """
        pk = kwargs.get('pk')
        serializer = self.serializer_class(Page.objects(id=pk)[0])
        return Response(serializer.data)

    def list(self, request):
        serializer = self.serializer_class(Page.objects.all(), many=True)
        return Response(dict(list_page=serializer.data))

    @list_route(methods=['post'])
    def get_element_by_page(self, request, *args, **kwargs):
        serializer_class = ElementSerializer
        pk = request.data.get('id', None)
        page = Page.objects(id=pk)[0]
        list_element = page.listElement
        serializer = serializer_class(list_element, many=True)
        return Response(dict(listElement=serializer.data))

    @list_route(methods=['post'])
    def start_test(self, request):
        """
        @apiVersion 1.0.0
        @api {POST} /page/start_test Send data to API
        @apiName Post send data
        @apiGroup shinobi_api
        @apiPermission IsAuthenticated
        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Authenticated Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": "1",
            "Agent": "Samsung A5 2016, Android app, build_number other_info",
            "Authorization": "token QS7VF3JF29K22U1IY7LAYLNKRW66BNSWF9CH4BND"
        }

        @apiSuccess {json} result
        """
        data = request.data.copy()
        url = request.data.get('url', None)
        dom = request.data.get('dom', None)
        id = "1"
        if url == None:
            raise Exception('Url is required')
        if dom == None:
            raise Exception('DOM structure is required')
        if 'full_screen' in request.data:
            saved = convertBase64toImg(request.data.get('full_screen'), id, 'image/%s', full_screen=True)
        else:
            raise Exception('Full screen is required')
        data['full_screen'] = get_image_url(saved['full_screen'])
        data['dom_origin'] = dom
        data['dom_origin_md5'] = PageService.computeMD5hash(dom)
        data['dom_reduce_md5'] = PageService.computeMD5hash(PageService.reduceTextHTML(dom))
        data['leaves_node'] = PageService.countLeavesNode(dom)
        data['max_depth'] = PageService.getMaxDepthTree(dom)
        data['histogram_color'] = PageService.getHistogramColor(saved['full_screen'])
        # check page was exists
        result = PageService.checkPage(data)
        print(result)
        page = result['page']
        warning_changed = result['warning_changed']
        if page == None:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            page = serializer.save()
            # save technology page
            data["id_page"] = page["id"]
            print(data["id_page"])
            page_technology_serializer = PageTechnologySerializer(data=data)
            page_technology_serializer.is_valid(raise_exception=True)
            page_technology = page_technology_serializer.save()
            page_data = self.serializer_class(page).data
            response = {
                'page': page_data,
                'warning_changed': False
            }
            return Response(response)
        else:
            if warning_changed:
                page_old = self.serializer_class(page)
                page_new = self.serializer_class(data=data)
                page_new.is_valid(raise_exception=True)
                response = {
                    'page-old': page_old.data,
                    'page-new': page_new.data,
                    'warning_changed': True
                }
            else:
                os.remove('{0}/{1}'.format(settings.MEDIA_ROOT, saved['full_screen']))
                page_data = self.serializer_class(page).data
                response = {
                    'page': page_data,
                    'warning_changed': False
                }
                print(page_data["id"])
            return Response(response)

    @list_route(methods=['post'])
    def update_tested(self, request):
        """
        @apiVersion 1.0.0
        @api {GET} /page/update_tested
        @apiName Get list
        @apiGroup shinobi_api
        @apiPermission IsManager
        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Authenticated Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": "1",
            "Agent": "Samsung A5 2016, Android app, build_number other_info",
            "Authorization": "token QS7VF3JF29K22U1IY7LAYLNKRW66BNSWF9CH4BND"
        }

        @apiSuccess {object[]} result
        """
        data = request.data.copy()
        page_testing = Page.objects(id=data['id_page'])[0]
        data_update = self.serializer_class(page_testing).data
        data_update['listElement'] = data["listElement"]
        id = "1"
        if 'test_screen' in data:
            saved = convertBase64toImg(data['test_screen'], id, 'image/%s', test_screen=True)
            if page_testing['test_screen'] != None:
                os.remove('{0}/{1}'.format(settings.MEDIA_ROOT, page_testing['test_screen'][-44:]))
            data_update['test_screen'] = get_image_url(saved['test_screen'])
        serializer = self.serializer_class(page_testing, data=data_update, partial=True)
        serializer.is_valid(raise_exception=True)
        page_testing = serializer.save()
        response = self.serializer_class(page_testing)
        return Response(response.data)
