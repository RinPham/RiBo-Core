from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ribo_api.models.task import Task
from ribo_api.models.user import User
from ribo_api.serializers.task import TaskSerializer
from ribo_api.services.utils import Utils


class TaskViewSet(ViewSet):
    view_set = 'task'
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
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
            user_id = request.GET.get('user_id','')
            tasks = Task.objects(user_id=user_id)
            serializer = self.serializer_class(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def create(self, request, *args, **kwargs):
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
            data = request.data.copy()
            data['intent_id'] = "5aa810bfe3d8ee4f97613dfa"
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def update(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /user update user
        @apiName update
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
            data = request.data.copy()
            task = Task.objects(id = data.get('id', None))[0]
            serializer = self.serializer_class(task, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            Utils.log_exception(e)
            raise e

    def delete(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /user update user
        @apiName update
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
            data = request.data.copy()
            pk = data.get('id', None)
            task = Task.objects(id = pk)
            if len(task) == 0:
                return Response("Id is wrong!", status=404)
            task.delete()
            return Response("Success")
        except Exception as e:
            Utils.log_exception(e)
            raise e