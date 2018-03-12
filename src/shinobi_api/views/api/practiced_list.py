from rest_framework.response import Response
from shinobi_api.views import BaseViewSet
from shinobi_api.serializers.practiced_list import PracticedListSerializer
from shinobi_api.models.practiced_list import PracticedList

class PracticedView(BaseViewSet):
    view_set = 'list-practiced'
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = ()

    # @list_route(methods=['get'])
    def list(self, request):
        """
        @apiVersion 1.0.0
        @api {GET} /practiced-list
        @apiName Get list
        @apiGroup VMS_API Admin_Visitor
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

        @apiSuccess {object[]} practiced_list
        @apiSuccess {string} type
        @apiSuccess {string[]} labels
        @apiSuccess {string[]} practiced_list
        """
        practiced_list = PracticedListSerializer(PracticedList.objects, many=True).data
        response_data = {
            'practiced_list': practiced_list,
        }
        return Response(response_data)